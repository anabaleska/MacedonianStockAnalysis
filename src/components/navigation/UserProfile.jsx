import React from 'react';
import styles from './UserProfile.module.css';

export const UserProfile = ({avatarSrc, userName}) => {
    return (
        <div className={styles.container}>
            <img
                loading="lazy"
                src={avatarSrc}
                className={styles.avatar}
                alt={`${userName}'s profile picture`}
            />
            <div className={styles.greeting}>
                <div className={styles.hello}>Hello,</div>
                <div className={styles.name}>{userName}</div>
            </div>
        </div>
    );
};