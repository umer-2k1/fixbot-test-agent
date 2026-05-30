# Self-hosted Browser-Use + Playwright Chromium (no Browser Use Cloud)
FROM python:3.12-bookworm

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
	PYTHONDONTWRITEBYTECODE=1 \
	IN_DOCKER=1 \
	BROWSER_USE_CHROME_NO_SANDBOX=1 \
	BROWSER_USE_HEADLESS=true \
	PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# Playwright system dependencies for Chromium
RUN apt-get update && apt-get install -y --no-install-recommends \
	ca-certificates \
	curl \
	&& rm -rf /var/lib/apt/lists/*

COPY requirements.docker.txt .
RUN pip install --no-cache-dir -r requirements.docker.txt \
	&& mkdir -p /ms-playwright \
	&& python -m playwright install --with-deps chromium

# Playwright 1.57+ uses chrome-linux64; older browser-use paths expect chrome-linux
RUN for dir in /ms-playwright/chromium-*/ /root/.cache/ms-playwright/chromium-*/; do \
	if [ -d "${dir}chrome-linux64" ] && [ ! -e "${dir}chrome-linux" ]; then \
	ln -sfn chrome-linux64 "${dir}chrome-linux"; \
	echo "Symlink: ${dir}chrome-linux -> chrome-linux64"; \
	fi; \
	done

# Verify Chromium is present before copying app code
RUN test -n "$(find /ms-playwright -name chrome -type f 2>/dev/null | head -1)" \
	|| test -n "$(find /ms-playwright -path '*chrome-linux*' -name chrome -type f 2>/dev/null | head -1)" \
	|| (echo "Chromium binary not found under /ms-playwright" && exit 1)

COPY app/ /app/

RUN useradd -m -u 1000 agentuser \
	&& chown -R agentuser:agentuser /app /ms-playwright

USER agentuser

CMD ["python", "main.py"]
