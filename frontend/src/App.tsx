import "./App.css";
import { useState } from "react";
import drugsJson from "./data/drugs.json";
import { Flashcard } from "./Flashcard";

export type Drug = {
	id: string;
	genericName: string;
	brandName: string;
	therapeuticClass: string;
	dosageFormsAndStrengths: string | null;
	category: string;
	moduleName: string;
};

const drugs = drugsJson as Drug[];

// Fisher-Yates shuffle algorithm
function shuffle<T>(items: T[]): T[] {
	const copy = [...items];
	for (let i = copy.length - 1; i > 0; i--) {
		const j = Math.floor(Math.random() * (i + 1));
		[copy[i], copy[j]] = [copy[j], copy[i]];
	}
	return copy;
}

function App() {
	const [index, setIndex] = useState(0);
	const [shuffledDrugs, setShuffledDrugs] = useState<Drug[]>(() =>
		shuffle(drugs),
	);
	const [revealed, setRevealed] = useState(false);
	const next = () => {
		setIndex((i) => (i + 1) % shuffledDrugs.length);
		setRevealed(false);
	};
	const prev = () => {
		setIndex((i) => (i - 1 + shuffledDrugs.length) % shuffledDrugs.length);
		setRevealed(false);
	};

	const reveal = () => setRevealed(true);
	return (
		<div>
			<Flashcard drug={shuffledDrugs[index]} revealed={revealed} />
			<button className="button" onClick={prev}>
				Previous
			</button>
			<button className="button" onClick={next}>
				Next
			</button>
			<button className="button" onClick={reveal}>
				Reveal
			</button>
		</div>
	);
}

export default App;
