import type { ReactNode } from 'react';

import './style.scss';

interface CardProps {
    title:string
    children?: ReactNode
}

export function Card({title, children}:CardProps){
    return (
        <div className='card'>
            <h2>{title}</h2>
            {children}
        </div>
    )
}