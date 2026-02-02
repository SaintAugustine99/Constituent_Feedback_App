import React, { createContext, useState, useContext } from 'react';

const AssistantContext = createContext();

export function AssistantProvider({ children }) {
  const [activeInstrumentId, setActiveInstrumentId] = useState(null);

  return (
    <AssistantContext.Provider value={{ activeInstrumentId, setActiveInstrumentId }}>
      {children}
    </AssistantContext.Provider>
  );
}

export function useAssistant() {
  return useContext(AssistantContext);
}

export default AssistantContext;
