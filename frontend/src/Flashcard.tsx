import type { Drug } from "./App";

type FlashcardProps = {
	drug: Drug;
	revealed: boolean;
};

export function Flashcard({ drug, revealed }: FlashcardProps) {
	return (
		<div className="flashcard">
			<h2>Generic Name: {drug.genericName}</h2>

			{revealed ? (
				<div className="answers">
					<p>Brand Name: {drug.brandName}</p>
					<p>Therapeutic Class: {drug.therapeuticClass}</p>
					<p>Dosage Forms and Strengths: {drug.dosageFormsAndStrengths}</p>
					<p>Category: {drug.category}</p>
					<p>Module Name: {drug.moduleName}</p>
				</div>
			) : (
				<p className="hint">Click Reveal to see the answer</p>
			)}
		</div>
	);
}
