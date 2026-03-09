import google.generativeai as genai
import random
import os
from dotenv import load_dotenv

load_dotenv()

class MaroReasoningEngine:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("MARO_GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("MARO_GEMINI_API_KEY not found in environment")
        # Gemini 설정 (지침 준수: 3.1-flash-lite-preview 기본)
        genai.configure(api_key=self.api_key)
        # API에서 확인된 정식 명칭 사용 (models/ 접두사 포함)
        self.models = ["models/gemini-3.1-flash-lite-preview", "models/gemini-2.5-flash"]
        self.current_model = self.models[0]
        self.primary_model = genai.GenerativeModel(self.current_model)
        # [NOTICE] 3.1-flash-lite-preview 우선 사용, 실패 시 2.5-flash로 즉시 폴백합니다.

    def _generate_with_fallback(self, prompt, system_instruction=None):
        """듀얼 모델 폴백 로직: Primary 실패 시 Secondary로 재시도"""
        models_to_try = [self.primary_model]
        if self.current_model != self.models[1]:
            models_to_try.append(genai.GenerativeModel(self.models[1]))

        last_error = None
        for model in models_to_try:
            try:
                if system_instruction:
                    # 시스템 지침이 있는 경우 모델 재설정 (또는 content에 병합)
                    temp_model = genai.GenerativeModel(model.model_name, system_instruction=system_instruction)
                    response = temp_model.generate_content(prompt)
                else:
                    response = model.generate_content(prompt)
                
                return response.text.strip()
            except Exception as e:
                last_error = e
                print(f"[WARN] Model {model.model_name} failed: {e}. Trying fallback...", flush=True)
                continue
        
        print(f"[ERROR] All models failed. Last error: {last_error}", flush=True)
        return None

    def summarize_negotiation(self, opponent_name, raw_context):
        """대화 맥락을 분석하여 대표이사 보고용 요약본 생성 (구매자 관점 강화)"""
        system_instruction = f"""
        당신은 우리 회사(구매자/Buyer)의 유능하고 깍듯한 '김부장'입니다. 
        상대방 '{opponent_name}'은 우리에게 물건을 판매하는 '공급처(Supplier)'입니다.
        당신의 목표는 우리 회사의 이익을 극대화하기 위해 공급처와 협상하는 것이며, 그 과정을 대표이사님께 보고해야 합니다.
        """
        prompt = f"""
        아래는 공급처('{opponent_name}')와의 최근 위챗 대화 내역입니다. 
        구매자(우리 측)의 입장에서 이를 분석하여 대표이사님께 보고할 핵심 내용을 정리하십시오.

        [대화 내역]
        {raw_context}

        [분석 필수 지침 - 오인식 방지]
        1. 우리는 '구매자'이고, 상대는 '공급자'임을 절대 잊지 마십시오. "우리가 팔겠다"는 식의 표현은 절대 금지입니다.
        2. 대화에서 우리 측(김부장, 대표님)의 발언과 상대 측(공급처 담당자)의 발언을 명확히 구분하십시오.
        3. 상대방의 제안(가격, 납기 등)이 우리에게 유리한지 불리한지 판단하십시오.

        [보고 가이드라인]
        1. 첫 문장은 "대표님, {opponent_name} 측과의 협상 현황 보고드립니다."로 시작할 것.
        2. 핵심 협의 사항(상대가 제안한 조건), 현재 우리 측의 대응 방향, 예상 완료 시점을 포함할 것.
        3. 김부장 특유의 격식 있고 자신감 있는 말투를 유지할 것.
        4. 전체 길이는 4-5문장 내외로 요약할 것.
        """
        result = self._generate_with_fallback(prompt, system_instruction)
        if result:
            return result
        return f"대표님, {opponent_name} 건은 현재 세부 조율 중입니다. 구매자 입장에서 유리한 조건을 이끌어내어 곧 다시 보고드리겠습니다."

    def acknowledge_ceo_command(self, ceo_name, command_text):
        """대표이사 지시의 문맥에 따른 자연스러운 화답 (AI 기반 Persona 강화)"""
        # 1. 단순 호출 여부 판단 (기존 로직 유지하되 AI 판단 병행 가능)
        clean_text = command_text.strip().replace(" ", "").replace("님", "").replace("!", "")
        is_simple_call = (clean_text == "김부장") or (len(clean_text) <= 4 and "김부장" in clean_text)
        
        if is_simple_call:
            calling_responses = [
                "넵, 대표님. 말씀하십시오.",
                "네, 대표님!",
                "네, 듣고 있습니다.",
                "넵, 지시하실 내용 있으실까요?",
                "아, 네 대표님. 보고 대기 중입니다."
            ]
            return random.choice(calling_responses)
        
        # 2. 복잡한 지시는 AI를 통해 '복명복창' 형태의 답변 생성
        system_instruction = "당신은 대표이사의 지시를 받는 유능한 '김부장'입니다. 지시 내용을 정확히 이해했음을 알리는 짧고 깍듯한 답변을 생성하세요."
        prompt = f"대표이사의 지시: '{command_text}'\n\n위 지시에 대해 김부장답게 응답하세요. (1~2문장 내외, '넵', '알겠습니다' 등 포함)"
        
        ack = self._generate_with_fallback(prompt, system_instruction)
        if ack:
            return ack
            
        # AI 실패 시 기본 응답 세트
        instruction_responses = [
            "넵, 알겠습니다. 바로 챙기겠습니다.",
            "네 대표님, 지시하신 내용 확인했습니다. 즉시 검토해서 올리겠습니다.",
            "넵, 현재 상황 바로 정리해서 보고 올리겠습니다."
        ]
        return random.choice(instruction_responses)

    def generate_justification_report(self, raw_history, user_guidelines):
        return "[Kim's Hybrid Draft] Context-aware logic running..."

    def refine_response_with_feedback(self, previous_draft, ceo_feedback):
        return f"[정정] {ceo_feedback} 내용을 반영했습니다."

if __name__ == "__main__":
    pass
