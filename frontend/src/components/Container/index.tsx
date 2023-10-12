import { ReactNode } from 'react';

import "./index.scss"

interface ContainerProps {
	children: ReactNode
}
export function Container({children}: ContainerProps) {
	return (
		<main>
			{children}
		</main>
	);
}