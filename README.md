Every machine learning journey doesn’t end with training a model — in fact, that’s only half the battle. The real challenge lies in deployment: taking a model out of a notebook and putting it into the hands of real users.

That was the motive behind this project. I didn’t build a new model from scratch — the model I used was already trained by someone else. Instead, I deliberately picked up an existing model so I could focus entirely on the deployment pipeline. My goal was to gain hands‑on experience in packaging, serving, and exposing a model through a web interface that anyone could access.

The story unfolded with errors, retries, and breakthroughs: missing files, wrong Git branches, 404s, 502 Bad Gateways, and the infamous KeyError: 'bmi'. Each error was a lesson in debugging and deployment discipline. Finally, exposing port 8000 on RunPod gave me a public link I could share — and the project was live.
