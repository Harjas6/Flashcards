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
					<ul>
						<li>Brand Name: {drug.brandName}</li>
						<li>Therapeutic Class: {drug.therapeuticClass}</li>
						<li>Dosage Forms and Strengths: {drug.dosageFormsAndStrengths}</li>
						<li>Category: {drug.category}</li>
						<li>Module Name: {drug.moduleName}</li>
					</ul>
				</div>
			) : (
				<p className="hint">Click Reveal to see the answer</p>
			)}
		</div>
	);
}
