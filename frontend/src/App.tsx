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
const uniqueDrugModules = [...new Set(drugs.map((drug) => drug.moduleName))];

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
	const [selectedModule, setSelectedModule] = useState("all");
	const [uniqueCategories, setUniqueCategories] = useState<string[]>([
		...new Set(drugs.map((drug) => drug.category)),
	]);
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
	const reset = () => {
		setShuffledDrugs(shuffle(drugs));
		setIndex(0);
		setRevealed(false);
	};
	const reveal = () => setRevealed(true);
	const selectModules = (event: React.ChangeEvent<HTMLSelectElement>) => {
		const value = event.target.value;
		setSelectedModule(value);
		const filteredDrugs = drugs.filter(
			(drug) => value === "all" || drug.moduleName === value,
		);
		setUniqueCategories([
			...new Set(filteredDrugs.map((drug) => drug.category)),
		]);
		setShuffledDrugs(shuffle(filteredDrugs));
		setIndex(0);
		setRevealed(false);
	};

	const selectCategories = (event: React.ChangeEvent<HTMLSelectElement>) => {
		const value = event.target.value;
		const filteredDrugs = drugs.filter(
			(drug) =>
				(value === "all" && drug.moduleName === selectedModule) ||
				(drug.category === value && drug.moduleName === selectedModule),
		);
		setShuffledDrugs(shuffle(filteredDrugs));
		setIndex(0);
		setRevealed(false);
	};
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
			<button className="button" onClick={reset}>
				Shuffle
			</button>
			<label htmlFor="module-select">Filter by Module:</label>
			<select
				className="button"
				id="module-select"
				onChange={selectModules}
				defaultValue="all"
			>
				<option key="all" value="all">
					All
				</option>
				{uniqueDrugModules.map((category) => (
					<option key={category} value={category}>
						{category}
					</option>
				))}
			</select>
			{selectedModule !== "all" && (
				<>
					<label htmlFor="category-select">Filter by Category:</label>
					<select
						className="button"
						onChange={selectCategories}
						defaultValue="all"
					>
						<option key="all" value="all">
							All
						</option>
						{uniqueCategories.map((category) => (
							<option key={category} value={category}>
								{category}
							</option>
						))}
					</select>
				</>
			)}
		</div>
	);
}

export default App;
