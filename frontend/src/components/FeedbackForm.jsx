import React, { useState, useContext, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { legislationService, locationService } from '../services/api';

const FeedbackForm = ({ instrumentId, instrumentTitle }) => {
    const { user } = useContext(AuthContext);
    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        full_name: user?.username || '',
        constituency: user?.ward || '',
        ward: '',
        position: 'SUPPORT',
        comments: '',
        target_clause: '',
        proposed_alternative: '',
        image_evidence: null
    });
    const [status, setStatus] = useState('idle');

    // Guest location dropdowns
    const [counties, setCounties] = useState([]);
    const [constituencies, setConstituencies] = useState([]);
    const [wards, setWards] = useState([]);
    const [selectedCounty, setSelectedCounty] = useState('');
    const [selectedConstituency, setSelectedConstituency] = useState('');

    useEffect(() => {
        if (!user) {
            locationService.getCounties().then(data => {
                const results = data.results || data;
                setCounties(results);
            }).catch(() => {});
        }
    }, [user]);

    const handleCountyChange = async (countyId) => {
        setSelectedCounty(countyId);
        setSelectedConstituency('');
        setWards([]);
        if (countyId) {
            const data = await locationService.getConstituencies(countyId);
            setConstituencies(data.results || data);
        } else {
            setConstituencies([]);
        }
    };

    const handleConstituencyChange = async (constituencyId) => {
        setSelectedConstituency(constituencyId);
        const selected = constituencies.find(c => c.id === parseInt(constituencyId));
        setFormData(prev => ({ ...prev, constituency: selected?.name || '' }));
        if (constituencyId) {
            const data = await locationService.getWards(constituencyId);
            setWards(data.results || data);
        } else {
            setWards([]);
        }
    };

    const handleChange = (e) => {
        if (e.target.name === 'image_evidence') {
            setFormData({ ...formData, image_evidence: e.target.files[0] });
        } else {
            setFormData({ ...formData, [e.target.name]: e.target.value });
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setStatus('submitting');

        const data = new FormData();
        data.append('instrument', instrumentId);
        data.append('full_name', formData.full_name);
        data.append('constituency', formData.constituency);
        data.append('ward', formData.ward);
        data.append('position', formData.position);
        data.append('comments', formData.comments);
        if (formData.position === 'AMEND') {
            data.append('target_clause', formData.target_clause);
            data.append('proposed_alternative', formData.proposed_alternative);
        }
        if (formData.image_evidence) {
            data.append('image_evidence', formData.image_evidence);
        }

        try {
            await legislationService.submitFeedback(data);
            setStatus('success');
            setFormData({
                full_name: user?.username || '',
                constituency: user?.ward || '',
                ward: '',
                position: 'SUPPORT',
                comments: '',
                target_clause: '',
                proposed_alternative: '',
                image_evidence: null
            });
        } catch (err) {
            setStatus('error');
        }
    };

    // Success View
    if (status === 'success') {
        return (
            <div className="p-4 bg-green-100 text-green-700 rounded-lg">
                <h3 className="font-bold">Thank you{user ? `, ${user.username}` : ''}!</h3>
                <p>Your participation on "{instrumentTitle}" has been recorded.</p>
                <button onClick={() => setStatus('idle')} className="text-sm underline mt-2">Submit another?</button>
            </div>
        );
    }

    return (
        <form onSubmit={handleSubmit} className="space-y-4 bg-white p-6 rounded shadow-md mt-4 border-t-4 border-blue-600">
            <h3 className="text-xl font-bold text-gray-800">Submit Your Views</h3>
            <p className="text-sm text-gray-500">Participating in: <span className="font-semibold">{instrumentTitle}</span></p>

            {!user && (
                <div className="p-3 bg-blue-50 border border-blue-200 rounded-md text-sm text-blue-800">
                    Submitting as a guest. <button type="button" onClick={() => navigate('/login')} className="underline font-semibold">Login</button> or <button type="button" onClick={() => navigate('/register')} className="underline font-semibold">register</button> for a faster experience next time.
                </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <label className="block text-sm font-medium text-gray-700">Full Name</label>
                    <input
                        required
                        name="full_name"
                        value={formData.full_name}
                        onChange={handleChange}
                        readOnly={!!user}
                        className="mt-1 block w-full border border-gray-300 rounded-md p-2"
                    />
                </div>

                {user ? (
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Constituency / Ward</label>
                        <input
                            required
                            name="constituency"
                            value={formData.constituency}
                            onChange={handleChange}
                            readOnly
                            className="mt-1 block w-full border border-gray-300 rounded-md p-2 bg-gray-50"
                        />
                    </div>
                ) : (
                    <>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">County</label>
                            <select
                                value={selectedCounty}
                                onChange={(e) => handleCountyChange(e.target.value)}
                                className="mt-1 block w-full border border-gray-300 rounded-md p-2 bg-white"
                            >
                                <option value="">Select County</option>
                                {counties.map(c => (
                                    <option key={c.id} value={c.id}>{c.name}</option>
                                ))}
                            </select>
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Constituency</label>
                            <select
                                value={selectedConstituency}
                                onChange={(e) => handleConstituencyChange(e.target.value)}
                                className="mt-1 block w-full border border-gray-300 rounded-md p-2 bg-white"
                                disabled={!selectedCounty}
                            >
                                <option value="">Select Constituency</option>
                                {constituencies.map(c => (
                                    <option key={c.id} value={c.id}>{c.name}</option>
                                ))}
                            </select>
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Ward</label>
                            <select
                                name="ward"
                                value={formData.ward}
                                onChange={(e) => {
                                    const selected = wards.find(w => w.name === e.target.value);
                                    setFormData(prev => ({ ...prev, ward: selected?.name || '' }));
                                }}
                                className="mt-1 block w-full border border-gray-300 rounded-md p-2 bg-white"
                                disabled={!selectedConstituency}
                            >
                                <option value="">Select Ward</option>
                                {wards.map(w => (
                                    <option key={w.id} value={w.name}>{w.name}</option>
                                ))}
                            </select>
                        </div>
                    </>
                )}
            </div>

            <div>
                <label className="block text-sm font-medium text-gray-700">Your Position</label>
                <select name="position" value={formData.position} onChange={handleChange} className="mt-1 block w-full border border-gray-300 rounded-md p-2 bg-white">
                    <option value="SUPPORT">I Support this</option>
                    <option value="OPPOSE">I Oppose this</option>
                    <option value="AMEND">I Propose Amendments</option>
                </select>
            </div>

            {formData.position === 'AMEND' && (
                <>
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Which clause/section?</label>
                        <input
                            name="target_clause"
                            value={formData.target_clause}
                            onChange={handleChange}
                            placeholder="e.g. Section 12(3)(a)"
                            className="mt-1 block w-full border border-gray-300 rounded-md p-2"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Proposed Alternative</label>
                        <textarea
                            name="proposed_alternative"
                            rows="3"
                            value={formData.proposed_alternative}
                            onChange={handleChange}
                            placeholder="Describe your proposed change..."
                            className="mt-1 block w-full border border-gray-300 rounded-md p-2"
                        />
                    </div>
                </>
            )}

            <div>
                <label className="block text-sm font-medium text-gray-700">Comments / Memorandum</label>
                <textarea required name="comments" rows="4" value={formData.comments} onChange={handleChange} className="mt-1 block w-full border border-gray-300 rounded-md p-2" placeholder="State your reasons clearly..." />
            </div>

            <div>
                <label className="block text-sm font-medium text-gray-700">Attach Evidence (Optional)</label>
                <div className="mt-1 flex items-center">
                    <input type="file" name="image_evidence" accept="image/*" onChange={handleChange} className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100" />
                </div>
                <p className="text-xs text-gray-500 mt-1">Upload photos of documents or physical sites relevant to your feedback.</p>
            </div>

            <button disabled={status === 'submitting'} type="submit" className="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition disabled:bg-gray-400">
                {status === 'submitting' ? 'Submitting...' : 'Submit to Committee'}
            </button>

            {status === 'error' && <p className="text-red-500 text-sm">Something went wrong. Please try again.</p>}
        </form>
    );
};

export default FeedbackForm;
