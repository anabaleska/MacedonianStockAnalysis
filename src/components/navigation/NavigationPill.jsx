import React from 'react';
import styles from './NavigationPill.module.css';
import {Link} from "react-router-dom";

export const NavigationPill = ({label, path, isActive}) => {
    return (
        <Link to={path} className={`${styles.pill} ${isActive ? styles.active : styles.default} `}>
            {label}
        </Link>
    );
};