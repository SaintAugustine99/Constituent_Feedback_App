import React, { useState } from 'react';
import useLegislation from '../hooks/useLegislation';
import FeedbackForm from '../components/FeedbackForm';

function LegislationDashboard() {
    // 1. Fetch the data using our hook (using activeOnly to filter)
    const { data: instruments, loading, error } = useLegislation('instruments', { activeOnly: true });

    // 2. State to track which law the user clicked on
    const [selectedInstrument, setSelectedInstrument] = useState(null);

    return (
        <div className="min-h-screen bg-gray-50 font-sans text-gray-900">
            <main className="max-w-6xl mx-auto p-6 grid grid-cols-1 lg:grid-cols-3 gap-8">

                {/* LEFT COLUMN: List of Active Participation Opportunities */}
                <div className="lg:col-span-1 space-y-4">
                    <h2 className="text-xl font-bold border-b pb-2 mb-4">Open Opportunities</h2>

                    {loading && <p>Loading instruments...</p>}
                    {error && <p className="text-red-500">Error loading data.</p>}

                    {instruments.map((item) => (
                        <div
                            key={item.id}
                            onClick={() => setSelectedInstrument(item)}
                            className={`p-4 rounded-lg cursor-pointer transition border ${selectedInstrument?.id === item.id
                                    ? 'bg-blue-50 border-blue-500 ring-1 ring-blue-500'
                                    : 'bg-white border-gray-200 hover:border-blue-300 hover:shadow'
                                }`}
                        >
                            <span className="text-xs font-bold text-blue-600 bg-blue-100 px-2 py-1 rounded-full">
                                {item.category_name}
                            </span>
                            <h3 className="font-bold mt-2 leading-snug">{item.title}</h3>
                            <p className="text-xs text-gray-500 mt-2">{item.docket_name}</p>
                            <p className="text-xs text-red-500 font-medium mt-1">
                                Deadline: {new Date(item.participation_deadline).toLocaleDateString()}
                            </p>
                        </div>
                    ))}
                </div>

                {/* RIGHT COLUMN: The Detail View & Feedback Form */}
                <div className="lg:col-span-2">
                    {selectedInstrument ? (
                        <div className="space-y-6 animate-fade-in">
                            {/* Bill Details Card */}
                            <div className="bg-white p-8 rounded-lg shadow border border-gray-200">
                                <div className="flex justify-between items-start">
                                    <div>
                                        <h2 className="text-2xl font-bold text-gray-800">{selectedInstrument.title}</h2>
                                        <p className="text-slate-500">{selectedInstrument.docket_name}</p>
                                    </div>
                                    <span className="bg-green-100 text-green-800 text-xs px-3 py-1 rounded-full font-bold uppercase tracking-wide">
                                        {selectedInstrument.current_status.replace('_', ' ')}
                                    </span>
                                </div>

                                <div className="mt-6 prose prose-blue max-w-none">
                                    <h4 className="text-sm uppercase text-gray-500 font-bold tracking-wider">Summary</h4>
                                    <p className="text-gray-700 mt-1">{selectedInstrument.summary_text || "No summary provided by the docket."}</p>
                                </div>

                                {/* Simulated Download Link */}
                                <div className="mt-6 pt-6 border-t flex gap-4">
                                    <button className="text-blue-600 font-medium text-sm flex items-center hover:underline">
                                        📄 Download Full Legal Text (PDF)
                                    </button>
                                    <button className="text-blue-600 font-medium text-sm flex items-center hover:underline">
                                        📊 View Previous Status Reports
                                    </button>
                                </div>
                            </div>

                            {/* THE FEEDBACK FORM */}
                            <FeedbackForm
                                instrumentId={selectedInstrument.id}
                                instrumentTitle={selectedInstrument.title}
                            />

                        </div>
                    ) : (
                        // Empty State
                        <div className="h-full flex items-center justify-center text-gray-400 bg-gray-50 border-2 border-dashed border-gray-200 rounded-lg p-12">
                            <div className="text-center">
                                <p className="text-lg">Select an item from the list to view details and submit your feedback.</p>
                            </div>
                        </div>
                    )}
                </div>
            </main>
        </div>
    );
}

export default LegislationDashboard;
