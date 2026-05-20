IMAGE ?= ghcr.io/open-resume/resume-generator
DATA ?= resume.yaml
OUTPUT ?= output

build:
	docker build -t resume-generator .

resume:
	mkdir -p $(OUTPUT)
	docker run --rm \
		-v "$(PWD)/$(DATA):/app/resume.yaml" \
		-v "$(PWD)/$(OUTPUT):/app/output" \
		$(IMAGE) \
		-d /app/resume.yaml $(ARGS)

resume-modern:
	$(MAKE) resume ARGS="-t modern"

resume-ats:
	$(MAKE) resume ARGS="-t ats"

cover-letter:
	mkdir -p $(OUTPUT)
	docker run --rm \
		-v "$(PWD)/$(DATA):/app/resume.yaml" \
		-v "$(PWD)/$(OUTPUT):/app/output" \
		--entrypoint python3 \
		$(IMAGE) \
		src/scripts/generate_cover_letter.py \
		-d /app/resume.yaml -o /app/output/cover-letter.md

themes:
	docker run --rm $(IMAGE) --list-themes

clean:
	rm -rf $(OUTPUT)

.PHONY: build resume resume-modern resume-ats cover-letter themes clean
