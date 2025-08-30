package main

import (
	"log"
	"os"
)

func main() {
	if len(os.Args) != 3 {
		log.Fatalf("Usage: preprocessor <source-dir> <output-json-file>")
	}

	sourceDir := os.Args[1]
	outputFile := os.Args[2]

	err := scripts.RunPreprocessor(sourceDir, outputFile)
	if err != nil {
		log.Fatalf("Preprocessor failed: %v", err)
	}

	log.Printf("Preprocessing complete. Output written to %s\n", outputFile)
}
