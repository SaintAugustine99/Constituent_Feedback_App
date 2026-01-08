const baseTheme = {
    fonts: {
        heading: '"Merriweather", serif',
        body: '"Inter", sans-serif',
    },
    borderRadius: '12px',
    transition: '0.3s cubic-bezier(0.2, 0.0, 0.2, 1)',
};

export const lightTheme = {
    ...baseTheme,
    colors: {
        bg: {
            primary: '#F9F8F4',   // Warm Alabaster
            secondary: '#EFECE5', // Beige Sidebar
            surface: '#FFFFFF',   // White Cards
        },
        brand: {
            dark: '#404F24',      // Deep Olive
            primary: '#556B2F',   // Olive
            light: '#8F9779',     // Sage
            washed: '#E3E8D9',    // Pale Green
        },
        accent: {
            gold: '#DAA520',      // Harvest Gold
            terra: '#BC5D41',     // Red Soil
        },
        text: {
            primary: '#2B2E2B',   // Ink Green
            secondary: '#5C615C', // Grey Green
        },
        border: 'rgba(85, 107, 47, 0.2)', // Subtle Olive border
    },
    shadows: {
        soft: '0 4px 20px rgba(64, 79, 36, 0.08)',
    },
};

export const darkTheme = {
    ...baseTheme,
    colors: {
        bg: {
            primary: '#121412',   // Deep Charcoal (Night)
            secondary: '#1A1D1A', // Slightly lighter sidebar
            surface: '#1F241F',   // Dark Olive Card
        },
        brand: {
            dark: '#E3E8D9',      // Light text for headers (inverted)
            primary: '#6B8E23',   // Lighter Olive for visibility
            light: '#556B2F',     // Muted Olive
            washed: '#2A332A',    // Dark Green highlight
        },
        accent: {
            gold: '#FFD700',      // Bright Gold (Stars)
            terra: '#CD5C5C',     // Indian Red
        },
        text: {
            primary: '#E0E0E0',   // Off-white
            secondary: '#A0A0A0', // Grey
        },
        border: 'rgba(255, 255, 255, 0.1)',
    },
    shadows: {
        soft: '0 4px 20px rgba(0, 0, 0, 0.4)',
    },
};
