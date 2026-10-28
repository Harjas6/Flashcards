import type { Drug } from "./App";

type FlashcardProps = {
	drug: Drug;
	revealed: boolean;
};

export function Flashcard({ drug, revealed }: FlashcardProps) {
	return (
		<div className="flashcard">
			<div className="question">
				<h2>Generic Name: {drug.genericName}</h2>
			</div>

			{revealed ? (
				<div className="answers">
					<ul>
						<li>
							Brand Name: <b>{drug.brandName}</b>
						</li>
						<li>
							Therapeutic Class: <b>{drug.therapeuticClass}</b>
						</li>
						<li>
							Dosage Forms: <b>{drug.dosageFormsAndStrengths}</b>
						</li>
						<li>
							Category: <b>{drug.category}</b>
						</li>
						<li>
							Module Name: <b>{drug.moduleName}</b>
						</li>
					</ul>
				</div>
			) : (
				<p className="hint">Click Reveal to see the answer</p>
			)}
		</div>
	);
}
