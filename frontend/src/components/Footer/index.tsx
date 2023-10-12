import "./index.scss"

interface FooterProps {
	version: string
}

export function Footer({version}:FooterProps) {
	return (
		<footer>
			<a href={`https://github.com/MainKronos/Sonarr-AnimeDownloader/releases/tag/${version}`} target="_blank">Ver. {version}</a>
		</footer>
	);
}