import flask
import flask_cors
import time

def run_clocks():
    app = flask.Flask(__name__)
    flask_cors.CORS(app)
    routes(app)
    app.run(host='0.0.0.0', port=5000)

def main():
    run_clocks()

def routes(app):
	@app.route('/')
	def index():
		return '''
		<!DOCTYPE html>
		<html>
			<head>
				<meta charset="UTF-8">
				<meta name="viewport" content="width=device-width, initial-scale=1.0">
				<script type="module" src="https://cdn.jsdelivr.net/gh/starfederation/datastar@1.0.0-RC.5/bundles/datastar.js"></script>
				<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js" integrity="sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI" crossorigin="anonymous"></script>
				<title>Demo Clocks</title>
			</head>
				<body>
				<div>
					<div>
						<div id="serverclock"
						data-on-load="@get('/server')">
							<h1>Server Clock</h1>
								<div id="servertime"></div>
						</div>
					</div>
					<div>
						<div id="clientclock"
						data-on-interval__duration.1s="@get('/client')">
							<h1>Client Clock</h1>
								<div id="clienttime">Client Clock Loading...</div>
						</div>
					</div>
					<div>
						<h1>Piggyback Clock</h1>
							<div data-text="$piggy">Piggyback Clock Loading...</div>
					</div>
				</div>
			</body>
			</html>
			'''

	@app.route('/server')
	def server_stream():
		def server_patch():
			while True:
				server_timer = time.strftime('%H:%M:%S')
				yield 'event: datastar-patch-elements\n'
				yield f'data: elements <div id="servertime">{server_timer}</div>\n\n'
				yield 'event: datastar-patch-signals\n'
				yield f'data: signals {{piggy: "{server_timer}"}}\n\n'
				time.sleep(1)
		return flask.Response(server_patch(), mimetype='text/event-stream')

	@app.route('/client')
	def client_stream():
		client_timer = time.strftime('%H:%M:%S')
		return f'<div id="clienttime">{client_timer}</div>\n\n'

if __name__ == "__main__":
    main()
