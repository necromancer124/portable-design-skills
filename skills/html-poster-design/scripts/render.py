"""Render trusted local HTML with Playwright. No browser installation is implicit."""
import argparse


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', help='Path to trusted local HTML')
    parser.add_argument('--output', required=True, help='Destination PNG')
    parser.add_argument('--browser', choices=('chromium', 'chrome', 'msedge'), default='chromium')
    parser.add_argument('--width', type=int, default=1080)
    parser.add_argument('--height', type=int, default=1350)
    parser.add_argument('--scale', type=float, default=2)
    parser.add_argument('--selector', help='Capture this element instead of the viewport')
    parser.add_argument('--full-page', action='store_true')
    parser.add_argument('--allow-network', action='store_true', help='Allow remote HTTP(S) assets')
    args = parser.parse_args()
    from pathlib import Path
    source = Path(args.input).expanduser().resolve()
    if not source.is_file():
        parser.error('Input HTML does not exist: ' + str(source))
    if source.suffix.lower() not in ('.html', '.htm'):
        parser.error('Input must be an HTML file')
    if Path(args.output).suffix.lower() != '.png':
        parser.error('Output must end in .png')
    if not 1 <= args.width <= 10000 or not 1 <= args.height <= 10000 or not 0 < args.scale <= 4:
        parser.error('Dimensions must be 1-10000 and scale must be greater than 0 and at most 4')
    if args.selector and args.full_page:
        parser.error('--selector and --full-page are mutually exclusive')
    return args


def render(args):
    from pathlib import Path
    import json
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise RuntimeError('Install Playwright: python -m pip install -r requirements-render.txt') from None
    source = Path(args.input).expanduser().resolve()
    destination = Path(args.output).expanduser().resolve()
    errors = []
    blocked = []
    with sync_playwright() as p:
        launch = {'headless': True}
        if args.browser != 'chromium':
            launch['channel'] = args.browser
        try:
            browser = p.chromium.launch(**launch)
        except Exception as exc:
            raise RuntimeError('Cannot launch browser. Install Chromium with python -m playwright install chromium, or select an installed --browser chrome or --browser msedge. ' + str(exc)) from None
        try:
            context = browser.new_context(viewport={'width': args.width, 'height': args.height}, device_scale_factor=args.scale)
            if not args.allow_network:
                def block_remote(route):
                    blocked.append(route.request.url)
                    route.abort()
                context.route('http://**/*', block_remote)
                context.route('https://**/*', block_remote)
            page = context.new_page()
            page.on('pageerror', lambda exc: errors.append(str(exc)))
            page.goto(source.as_uri(), wait_until='load', timeout=30000)
            page.evaluate('() => document.fonts.ready')
            page.evaluate('() => Promise.all([...document.images].map(i => i.decode().catch(() => null)))')
            broken = page.locator('img').evaluate_all('(imgs) => imgs.filter(i => !i.complete || i.naturalWidth === 0).map(i => i.getAttribute("src"))')
            if blocked:
                raise RuntimeError('Remote asset requests blocked; embed/download assets or explicitly use --allow-network.')
            if broken:
                raise RuntimeError('Broken images: ' + str(broken))
            if errors:
                raise RuntimeError('Page JavaScript errors: ' + '; '.join(errors))
            destination.parent.mkdir(parents=True, exist_ok=True)
            if args.selector:
                page.locator(args.selector).screenshot(path=str(destination), timeout=15000, animations='disabled')
            else:
                page.screenshot(path=str(destination), full_page=args.full_page, animations='disabled')
        finally:
            browser.close()
    print(json.dumps({'png': str(destination), 'browser': args.browser, 'viewport': [args.width, args.height], 'scale': args.scale, 'javascript_errors': errors}))


if __name__ == '__main__':
    import sys
    try:
        render(main())
    except Exception as exc:
        print('Render failed: ' + str(exc), file=sys.stderr)
        sys.exit(1)
