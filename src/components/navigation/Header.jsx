import React from 'react';
import styles from './Header.module.css';
import { NavigationPill } from './NavigationPill';
import { UserProfile } from './UserProfile';
import {useLocation} from "react-router-dom";
import { jwtDecode } from 'jwt-decode';

export const Header = () => {
    const token = localStorage.getItem('token');
    let isAdmin = false;

    if (token) {
        try {
            const decodedToken = jwtDecode(token);
            isAdmin = decodedToken.role === 'ADMIN'; // Check if the user has the admin role
        } catch (error) {
            console.error('Invalid token:', error);
        }
    }
    const location = useLocation();
    const navigationItems = [
        { label: 'Dashboard', path: '/', isActive: false },
        { label: 'Stocks History', isActive: true },
        { label: 'Predictions', path:'/predictions', isActive: false },
        { label: 'Admin', path: '/admin', isActive: false, Admin: true },
        { label: 'UserProfile', path: '/profile', isActive: false }
    ];

    return (
        <header className={styles.header}>
            <div className={styles.logo}>
                M<span className={styles.logoHighlight}>S</span>A
            </div>

            <form className={styles.searchContainer} role="search">
                <label htmlFor="searchInput" className="visually-hidden"></label>
                <input
                    id="searchInput"
                    type="search"
                    className={styles.searchInput}
                    placeholder="Search.."
                />
                <img
                    loading="lazy"
                    src="https://cdn.builder.io/api/v1/image/assets/TEMP/62a5072c383fb906a384a19cdedeecd8a80dbb4b731ad9dee4843da916cab0c6?placeholderIfAbsent=true&apiKey=60217a24597e419ca472b84d3fa7f5bd"
                    className={styles.searchIcon}
                    alt=""
                />
            </form>

            <nav className={styles.navigationList}>
                {navigationItems.map((item, index) => (
                    <NavigationPill
                        key={index}
                        label={item.label}
                        isActive={location.pathname === item.path}
                        path={item.path}
                        admin={isAdmin}
                    />
                ))}
            </nav>

            <div className={styles.userSection}>
                <UserProfile
                    avatarSrc="https://cdn.builder.io/api/v1/image/assets/TEMP/8e7c11bec8dc82f31a964d9646ac514f8e125c0e12ab070947a10ff5f3d896d5?placeholderIfAbsent=true&apiKey=60217a24597e419ca472b84d3fa7f5bd"
                    userName="Ana"
                />
                <div className={styles.notification} />
            </div>
        </header>
    );
};