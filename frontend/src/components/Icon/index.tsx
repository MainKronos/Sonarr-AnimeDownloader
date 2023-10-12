import "./index.scss"

interface IconProps {
	icon: string
}

export function Icon({icon}: IconProps) {
	return <i className="material-symbols-rounded">{icon}</i>;
}