import { useState, useEffect } from 'react';
import './App.css';
import {
    Users,
    ShieldCheck,
    LayoutDashboard,
    ChevronRight,
    Terminal,
    Plus,
    Search,
    X,
    Edit3,
    SendHorizontal,
    AlertCircle,
    MessageSquare,
    RefreshCw
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

function App() {
    const [activeSupplier, setActiveSupplier] = useState('Kimlead Jerry');
    const [isAddModalOpen, setIsAddModalOpen] = useState(false);
    const [newSupplierName, setNewSupplierName] = useState('');

    // CEO 피드백 및 정정 코멘트 상태
    const [ceoFeedback, setCeoFeedback] = useState('');
    const [isRegenerating, setIsRegenerating] = useState(false);
    const [logs, setLogs] = useState<any[]>([]);

    useEffect(() => {
        // 실시간 로그 페칭
        const fetchLogs = async () => {
            try {
                const response = await fetch('http://localhost:8000/logs/recent');
                const data = await response.json();
                setLogs(data);
            } catch (error) {
                console.error("Failed to fetch logs:", error);
            }
        };
        fetchLogs();
        const interval = setInterval(fetchLogs, 3000);
        return () => clearInterval(interval);
    }, []);

    // 에이전트 제안 답변 상태 관리
    const [proposedResponse, setProposedResponse] = useState(
        "제리, 6박스를 빼고 청구하는 건 보상이 아니야. 컨테이너 430박스를 다 실어줘. 다만 그중 6박스는 지난번 미납분으로 Zero 인보이스 처리해. 그리고 LSS/PSS 포함된 All-in 단가 다시 확인해주면 바로 계약할게."
    );

    const [suppliers, setSuppliers] = useState([
        { name: 'Kimlead Jerry', status: 'approval_required', lastSeen: '12:26' },
        { name: 'Byron', status: 'negotiating', lastSeen: 'Yesterday' },
        { name: 'LI KUN', status: 'idle', lastSeen: '2 days ago' }
    ]);

    const handleAddSupplier = () => {
        if (newSupplierName.trim()) {
            setSuppliers([...suppliers, { name: newSupplierName, status: 'idle', lastSeen: 'Just added' }]);
            setNewSupplierName('');
            setIsAddModalOpen(false);
        }
    };

    const handleRegenerate = () => {
        if (!ceoFeedback.trim()) {
            alert("에이전트에게 전달할 정정 코멘트를 입력해주세요.");
            return;
        }
        setIsRegenerating(true);
        // 시뮬레이션: 1.5초 후 피드백이 반영된 새로운 답변 생성
        setTimeout(() => {
            setProposedResponse(`[코멘트 반영됨] 제리, 대표님 지시대로 단가는 $2.20로 최종 제안할게. 6박스는 실물 보상해주고 LSS 포함 All-in으로 정리해서 인보이스 보내줘.`);
            setIsRegenerating(false);
            setCeoFeedback('');
        }, 1500);
    };

    const handleSendResponse = () => {
        alert(`[대표이사 최종 승인 완료]\n\n김부장 계정으로 다음 메시지를 ${activeSupplier}에게 발송합니다:\n\n"${proposedResponse}"`);
    };

    return (
        <div className="dashboard-container">
            {/* Sidebar */}
            <aside className="sidebar">
                <div className="logo-container">MARO AGENT</div>
                <div style={{ fontSize: '0.7rem', color: 'var(--accent-primary)', marginBottom: '1.5rem', fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: '5px' }}>
                    <ShieldCheck size={12} /> AWS-HOSTED PERSONA: MANAGER KIM
                </div>
                <nav>
                    <div className="nav-item active">
                        <LayoutDashboard size={20} style={{ marginRight: '12px' }} />
                        Dashboard
                    </div>
                    <div className="nav-item">
                        <Users size={20} style={{ marginRight: '12px' }} />
                        Suppliers
                    </div>
                </nav>

                <div style={{
                    marginTop: '2rem',
                    fontSize: '0.75rem',
                    color: 'var(--text-muted)',
                    marginBottom: '1rem',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center'
                }}>
                    REGISTERED TARGETS
                    <Plus
                        size={14}
                        style={{ cursor: 'pointer' }}
                        onClick={() => setIsAddModalOpen(true)}
                    />
                </div>

                {suppliers.map(s => (
                    <div
                        key={s.name}
                        className={`nav-item ${activeSupplier === s.name ? 'active' : ''}`}
                        onClick={() => setActiveSupplier(s.name)}
                    >
                        <div style={{
                            width: '8px',
                            height: '8px',
                            borderRadius: '50%',
                            backgroundColor: s.status === 'approval_required' ? 'var(--warning)' : s.status === 'negotiating' ? 'var(--success)' : '#52525b',
                            marginRight: '12px'
                        }}></div>
                        {s.name}
                    </div>
                ))}
            </aside>

            {/* Main Content */}
            <main className="main-content">
                <motion.div
                    key={activeSupplier}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5 }}
                >
                    <div className="report-header">
                        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                            <h2 style={{ fontSize: '1.5rem', fontWeight: '600' }}>Strategy Analysis: {activeSupplier}</h2>
                        </div>
                        {suppliers.find(s => s.name === activeSupplier)?.status === 'approval_required' && (
                            <div className="status-badge" style={{ backgroundColor: 'rgba(245, 158, 11, 0.1)', color: 'var(--warning)', border: '1px solid var(--warning)' }}>
                                CEO Approval Required
                            </div>
                        )}
                    </div>

                    <div className="card">
                        <h3 style={{ marginBottom: '1rem', display: 'flex', alignItems: 'center', fontSize: '1rem' }}>
                            <ShieldCheck size={20} color="var(--accent-primary)" style={{ marginRight: '10px' }} />
                            Agent Reasoning & Recommendation
                        </h3>
                        {activeSupplier === 'Kimlead Jerry' ? (
                            <>
                                <p style={{ color: 'var(--text-muted)', lineHeight: '1.6', marginBottom: '1.5rem', fontSize: '0.95rem' }}>
                                    공급사가 제안한 FOB 단가는 경쟁사 대비 2% 저렴해 보이나, <strong>LSS/PSS 할증료가 제외</strong>되어 실제 수입 원가는 약 3% 상승할 리스크가 감지되었습니다. 6박스 누락분에 대한 실물 보상과 All-in FOB 단가 재협상을 강력히 권고합니다.
                                </p>
                                <div style={{ borderTop: '1px solid var(--border)', paddingTop: '1rem' }}>
                                    <h4 style={{ fontSize: '0.85rem', marginBottom: '0.75rem', color: 'var(--text-main)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Key Strategic Insights</h4>
                                    <ul style={{ listStyle: 'none', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                                        <li style={{ marginBottom: '0.6rem', display: 'flex', alignItems: 'center' }}>
                                            <ChevronRight size={14} style={{ marginRight: '8px', color: 'var(--accent-primary)' }} /> 6박스 누락 청구 차감은 FCL 계약상 불리 (실물 추가 선적 필요)
                                        </li>
                                        <li style={{ display: 'flex', alignItems: 'center' }}>
                                            <ChevronRight size={14} style={{ marginRight: '8px', color: 'var(--accent-primary)' }} /> 할증료 포함 All-in 단가 타겟: $2.30 (Middle Point)
                                        </li>
                                    </ul>
                                </div>
                            </>
                        ) : (
                            <p style={{ color: 'var(--text-muted)', fontStyle: 'italic' }}>
                                {activeSupplier} 업체와 새로운 대화를 시작했습니다. 위챗에서 대화가 진행되면 실시간으로 분석이 시작됩니다.
                            </p>
                        )}
                    </div>

                    {activeSupplier === 'Kimlead Jerry' && (
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
                            {/* Feedback Loop Area */}
                            <div className="card" style={{ border: '1px solid rgba(245, 158, 11, 0.2)' }}>
                                <h3 style={{ marginBottom: '1rem', display: 'flex', alignItems: 'center', fontSize: '1rem' }}>
                                    <MessageSquare size={18} color="var(--warning)" style={{ marginRight: '10px' }} />
                                    CEO Corrective Comment
                                </h3>
                                <textarea
                                    className="response-editor"
                                    placeholder="추론 정보가 틀렸거나 추가 지시가 있다면 여기에 입력하세요... (예: 단가 $2.20로 조정할 것)"
                                    value={ceoFeedback}
                                    onChange={(e) => setCeoFeedback(e.target.value)}
                                    style={{ minHeight: '100px', fontSize: '0.9rem', background: 'rgba(245, 158, 11, 0.03)' }}
                                />
                                <button
                                    className="regenerate-btn"
                                    onClick={handleRegenerate}
                                    disabled={isRegenerating || !ceoFeedback.trim()}
                                    style={{
                                        width: '100%',
                                        marginTop: '1rem',
                                        padding: '0.75rem',
                                        background: 'rgba(245, 158, 11, 0.1)',
                                        border: '1px solid var(--warning)',
                                        color: 'var(--warning)',
                                        borderRadius: '0.5rem',
                                        cursor: 'pointer',
                                        display: 'flex',
                                        alignItems: 'center',
                                        justifyContent: 'center',
                                        gap: '8px',
                                        fontWeight: '600',
                                        transition: 'all 0.2s'
                                    }}
                                >
                                    <RefreshCw size={16} className={isRegenerating ? 'spin' : ''} />
                                    {isRegenerating ? '재추론 중...' : '지시 반영하여 다시 작성'}
                                </button>
                            </div>

                            {/* Proposed Response Area */}
                            <div className="card" style={{ border: '1px solid rgba(131, 58, 180, 0.3)', background: 'rgba(131, 58, 180, 0.08)' }}>
                                <h3 style={{ marginBottom: '1.25rem', display: 'flex', alignItems: 'center', fontSize: '1rem' }}>
                                    <Edit3 size={18} color="white" style={{ marginRight: '10px' }} />
                                    Proposed Response (Editable)
                                </h3>
                                <textarea
                                    className="response-editor"
                                    value={proposedResponse}
                                    onChange={(e) => setProposedResponse(e.target.value)}
                                    style={{ minHeight: '135px' }}
                                />
                                <div style={{ marginTop: '0.75rem', fontSize: '0.75rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '6px' }}>
                                    <AlertCircle size={14} /> 최종 승인 전 문구를 자유롭게 다듬으실 수 있습니다.
                                </div>
                            </div>
                        </div>
                    )}
                </motion.div>
            </main>

            {/* Right Stream Panel */}
            <section className="right-panel">
                <h3 style={{ fontSize: '0.9rem', fontWeight: '600', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                    <Terminal size={18} style={{ marginRight: '10px', color: 'var(--accent-primary)' }} />
                    Live Monitoring (Manager Kim)
                </h3>
                <div className="log-stream">
                    {logs.length > 0 ? logs.map((log, idx) => (
                        <div key={idx} className="log-entry">
                            <span style={{ color: 'var(--text-muted)', fontSize: '0.7rem' }}>[{log.timestamp}]</span>
                            <span style={{
                                color: log.type === 'KIM' ? 'var(--accent-primary)' : log.type === 'BOSS' ? '#ef4444' : '#60a5fa',
                                marginLeft: '8px',
                                fontWeight: 'bold'
                            }}>[{log.type}]</span> {log.message}
                        </div>
                    )) : (
                        <div className="log-entry" style={{ opacity: 0.5 }}>[SYSTEM] Waiting for dashboard API...</div>
                    )}
                </div>

                <div style={{ marginTop: 'auto' }}>
                    <button
                        className="approval-btn"
                        disabled={activeSupplier !== 'Kimlead Jerry' || isRegenerating}
                        style={{
                            opacity: (activeSupplier !== 'Kimlead Jerry' || isRegenerating) ? 0.3 : 1,
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            gap: '10px'
                        }}
                        onClick={handleSendResponse}
                    >
                        <SendHorizontal size={18} />
                        APPROVE &amp; SEND
                    </button>
                    <p style={{ fontSize: '0.65rem', color: 'var(--text-muted)', textAlign: 'center', marginTop: '1rem', lineHeight: '1.4' }}>
                        최종 승인된 본문은 {activeSupplier}님께<br /><strong>AWS 김부장 계정</strong>으로 즉시 전송됩니다.
                    </p>
                </div>
            </section>

            {/* Add Supplier Modal ... same as before ... */}
            <AnimatePresence>
                {isAddModalOpen && (
                    <motion.div className="modal-overlay" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.85)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000, backdropFilter: 'blur(8px)' }}>
                        <motion.div className="card" initial={{ scale: 0.95, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} exit={{ scale: 0.95, opacity: 0 }} style={{ width: '420px', padding: '2.5rem' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '2rem', alignItems: 'center' }}>
                                <h3 style={{ display: 'flex', alignItems: 'center', margin: 0 }}><Users size={20} style={{ marginRight: '12px', color: 'var(--accent-primary)' }} /> 협상 타겟 등록</h3>
                                <X style={{ cursor: 'pointer', opacity: 0.5 }} onClick={() => setIsAddModalOpen(false)} />
                            </div>
                            <div style={{ marginBottom: '2rem' }}>
                                <label style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block', marginBottom: '0.75rem', fontWeight: '500' }}>위챗 닉네임 (정확히 입력)</label>
                                <div style={{ position: 'relative' }}>
                                    <Search size={16} style={{ position: 'absolute', left: '16px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
                                    <input type="text" placeholder="공급사 이름 입력..." value={newSupplierName} onChange={(e) => setNewSupplierName(e.target.value)} onKeyPress={(e) => e.key === 'Enter' && handleAddSupplier()} style={{ width: '100%', padding: '1rem 1rem 1rem 3rem', background: '#0a0a0c', border: '1px solid var(--border)', borderRadius: '0.75rem', color: 'white', outline: 'none', fontSize: '0.9rem' }} />
                                </div>
                            </div>
                            <button className="approval-btn" onClick={handleAddSupplier} style={{ marginTop: 0 }}>타겟 등록 및 감시 시작</button>
                        </motion.div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}

export default App;
