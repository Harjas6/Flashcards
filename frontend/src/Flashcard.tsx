import type { Drug } from "./App";

type FlashcardProps = {
	drug: Drug;
	revealed: boolean;
};

export function Flashcard({ drug, revealed }: FlashcardProps) {
	return (
		<div className="flashcard">
			<h2>{drug.genericName}</h2>

			{revealed ? (
				<div className="answers">
					<p>{drug.brandName}</p>
					<p>{drug.therapeuticClass}</p>
					<p>{drug.dosageFormsAndStrengths}</p>
					<p>{drug.category}</p>
					<p>{drug.moduleName}</p>
				</div>
			) : (
				<p className="hint">Click Reveal to see the answer</p>
			)}
		</div>
	);
}
