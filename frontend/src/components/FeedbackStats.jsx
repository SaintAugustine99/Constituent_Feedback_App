import React, { useState, useEffect } from 'react';
import { legislationService } from '../services/api';

const FeedbackStats = ({ instrumentId }) => {
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!instrumentId) return;
        setLoading(true);
        legislationService.getInstrumentStats(instrumentId)
            .then(data => setStats(data))
            .catch(() => setStats(null))
            .finally(() => setLoading(false));
    }, [instrumentId]);

    if (loading || !stats || stats.total_feedback === 0) return null;

    const { positions, total_feedback } = stats;
    const supportPct = (positions.SUPPORT / total_feedback) * 100;
    const opposePct = (positions.OPPOSE / total_feedback) * 100;
    const amendPct = (positions.AMEND / total_feedback) * 100;

    return (
        <div style={{
            background: '#f8f9fa',
            borderRadius: '12px',
            padding: '1.25rem',
            marginBottom: '1.5rem',
            border: '1px solid #e9ecef'
        }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
                <h4 style={{ margin: 0, fontSize: '1rem', fontWeight: 600, color: '#333' }}>
                    Public Sentiment
                </h4>
                <span style={{ fontSize: '0.85rem', color: '#666' }}>
                    {total_feedback} submission{total_feedback !== 1 ? 's' : ''}
                </span>
            </div>

            {/* Progress bar */}
            <div style={{
                display: 'flex',
                height: '24px',
                borderRadius: '12px',
                overflow: 'hidden',
                marginBottom: '0.75rem',
                background: '#e9ecef'
            }}>
                {supportPct > 0 && (
                    <div style={{
                        width: `${supportPct}%`,
                        background: '#2e7d32',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        color: 'white',
                        fontSize: '0.7rem',
                        fontWeight: 700,
                        minWidth: supportPct > 8 ? 'auto' : '0',
                    }}>
                        {supportPct > 8 ? `${Math.round(supportPct)}%` : ''}
                    </div>
                )}
                {opposePct > 0 && (
                    <div style={{
                        width: `${opposePct}%`,
                        background: '#c62828',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        color: 'white',
                        fontSize: '0.7rem',
                        fontWeight: 700,
                        minWidth: opposePct > 8 ? 'auto' : '0',
                    }}>
                        {opposePct > 8 ? `${Math.round(opposePct)}%` : ''}
                    </div>
                )}
                {amendPct > 0 && (
                    <div style={{
                        width: `${amendPct}%`,
                        background: '#e65100',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        color: 'white',
                        fontSize: '0.7rem',
                        fontWeight: 700,
                        minWidth: amendPct > 8 ? 'auto' : '0',
                    }}>
                        {amendPct > 8 ? `${Math.round(amendPct)}%` : ''}
                    </div>
                )}
            </div>

            {/* Legend */}
            <div style={{ display: 'flex', gap: '1.5rem', fontSize: '0.85rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                    <span style={{ width: 12, height: 12, borderRadius: '50%', background: '#2e7d32', display: 'inline-block' }} />
                    <span>Support ({positions.SUPPORT})</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                    <span style={{ width: 12, height: 12, borderRadius: '50%', background: '#c62828', display: 'inline-block' }} />
                    <span>Oppose ({positions.OPPOSE})</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                    <span style={{ width: 12, height: 12, borderRadius: '50%', background: '#e65100', display: 'inline-block' }} />
                    <span>Amend ({positions.AMEND})</span>
                </div>
            </div>
        </div>
    );
};

export default FeedbackStats;
