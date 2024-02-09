import type { ReactNode } from 'react';

import './style.scss';

interface CardProps {
    className?: string
    children?: ReactNode
}

export function Card({children, className}:CardProps){
    return (
        <div className={`card ${className}`}>
            {children}
        </div>
    )
}