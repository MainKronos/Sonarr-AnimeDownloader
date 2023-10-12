import { ReactNode } from "react"
import { Icon } from ".."
import "./index.scss"

interface HeaderProps {
	title: string,
	children?: ReactNode
}

export function Header(props: HeaderProps) {
	return (
		<header>
			<h1>{props.title}</h1>

			<a id='donate' href="https://github.com/sponsors/MainKronos" target="_blank">
				<Icon icon="favorite"/>
			</a>

			{props.children}
		</header>
	)
}