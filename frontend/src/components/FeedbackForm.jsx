import React, { useState } from 'react';

const FeedbackForm = ({ instrumentId, instrumentTitle }) => {
    const [formData, setFormData] = useState({
        full_name: '',
        constituency: '',
        position: 'SUPPORT', // Default value
        comments: '',
        image_evidence: null
    });
    const [status, setStatus] = useState('idle'); // idle, submitting, success, error

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

        // We must use FormData because we are sending a file (image)
        const data = new FormData();
        data.append('instrument', instrumentId);
        data.append('full_name', formData.full_name);
        data.append('constituency', formData.constituency);
        data.append('position', formData.position);
        data.append('comments', formData.comments);
        if (formData.image_evidence) {
            data.append('image_evidence', formData.image_evidence);
        }

        try {
            const response = await fetch('http://localhost:8000/api/legislation/feedback/', {
                method: 'POST',
                body: data, // No headers needed; fetch sets multipart/form-data automatically
            });

            if (response.ok) {
                setStatus('success');
                setFormData({ full_name: '', constituency: '', position: 'SUPPORT', comments: '', image_evidence: null });
            } else {
                setStatus('error');
            }
        } catch (err) {
            setStatus('error');
        }
    };

    if (status === 'success') {
        return (
            <div className="p-4 bg-green-100 text-green-700 rounded-lg">
                <h3 className="font-bold">Thank you!</h3>
                <p>Your participation on "{instrumentTitle}" has been recorded.</p>
                <button onClick={() => setStatus('idle')} className="text-sm underline mt-2">Submit another?</button>
            </div>
        );
    }

    return (
        <form onSubmit={handleSubmit} className="space-y-4 bg-white p-6 rounded shadow-md mt-4 border-t-4 border-blue-600">
            <h3 className="text-xl font-bold text-gray-800">Submit Your Views</h3>
            <p className="text-sm text-gray-500">Participating in: <span className="font-semibold">{instrumentTitle}</span></p>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <label className="block text-sm font-medium text-gray-700">Full Name</label>
                    <input required name="full_name" value={formData.full_name} onChange={handleChange} className="mt-1 block w-full border border-gray-300 rounded-md p-2" />
                </div>
                <div>
                    <label className="block text-sm font-medium text-gray-700">Constituency / Ward</label>
                    <input required name="constituency" value={formData.constituency} onChange={handleChange} className="mt-1 block w-full border border-gray-300 rounded-md p-2" />
                </div>
            </div>

            <div>
                <label className="block text-sm font-medium text-gray-700">Your Position</label>
                <select name="position" value={formData.position} onChange={handleChange} className="mt-1 block w-full border border-gray-300 rounded-md p-2 bg-white">
                    <option value="SUPPORT">I Support this</option>
                    <option value="OPPOSE">I Oppose this</option>
                    <option value="AMEND">I Propose Amendments</option>
                </select>
            </div>

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
