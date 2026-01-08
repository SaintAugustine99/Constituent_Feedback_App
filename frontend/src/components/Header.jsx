import React, { useContext } from 'react'; // <--- Import useContext
import styled from 'styled-components';
import { Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext'; // <--- Import Context

// ... (Keep your HeaderWrapper, Logo, styles the same) ...
const HeaderWrapper = styled.header`
  padding: 1.5rem 2rem;
  background: ${({ theme }) => theme.colors.bg.surface}E6;
  border-bottom: 1px solid ${({ theme }) => theme.colors.brand.light}30;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(10px);
`;

const Logo = styled(Link)`
  font-family: ${({ theme }) => theme.fonts.heading};
  font-size: 2rem;
  font-weight: 900;
  text-decoration: none;
  background: linear-gradient(90deg, #000000 25%, #BB0000 50%, #006600 75%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
`;

const NavActions = styled.div`
  display: flex;
  align-items: center;
  gap: 1.5rem;
`;

const UserGreeting = styled.span`
  font-weight: 600;
  color: ${({ theme }) => theme.colors.brand.dark};
`;

const ThemeToggle = styled.button`
  background: none;
  border: 1px solid ${({ theme }) => theme.colors.brand.primary};
  color: ${({ theme }) => theme.colors.text.primary};
  padding: 0.5rem;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;

  &:hover {
    background: ${({ theme }) => theme.colors.brand.washed};
  }
`;

const ButtonLink = styled(Link)`
  text-decoration: none;
  color: ${({ theme }) => theme.colors.text.primary};
  font-weight: 600;
  &:hover { color: ${({ theme }) => theme.colors.brand.primary}; }
`;

const LogoutButton = styled.button`
  background: none;
  border: none;
  color: ${({ theme }) => theme.colors.accent.terra};
  font-weight: 600;
  cursor: pointer;
  font-family: inherit;
  font-size: 1rem;
`;

const Header = ({ toggleTheme, isDarkMode }) => {
    const { user, logout } = useContext(AuthContext); // <--- Use the Hook

    return (
        <HeaderWrapper>
            <Logo to="/">JAMII.</Logo>

            <NavActions>
                {user ? (
                    <>
                        <UserGreeting>Jambo, {user.username}</UserGreeting>
                        <LogoutButton onClick={logout}>Logout</LogoutButton>
                    </>
                ) : (
                    <>
                        <ButtonLink to="/login">Login</ButtonLink>
                        <ButtonLink to="/register">Register</ButtonLink>
                    </>
                )}

                <ThemeToggle onClick={toggleTheme}>
                    {isDarkMode ? '☀️' : '🌙'}
                </ThemeToggle>
            </NavActions>
        </HeaderWrapper>
    );
};

export default Header;
