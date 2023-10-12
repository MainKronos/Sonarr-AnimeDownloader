import { Component } from "react";
import { Header, Navigator } from "@/components";

export default class App extends Component {
	render() {
		return (
			<>
				<Header title="Settings"/>
				<Navigator>
					<a>Home</a>
					<a href="settings">Settings</a>
					<a href="log">Log</a>
				</Navigator>
			</>
		)
	}
}