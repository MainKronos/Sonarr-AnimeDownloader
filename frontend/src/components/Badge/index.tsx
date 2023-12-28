import './style.scss';

interface BadgeProps {
    title:string
}
export function Badge({title}:BadgeProps){
    return (
        <span className='badge'>{title}</span>
    )
}