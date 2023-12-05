It would be nice to be able to run console locally.

I'm not sure what the journey is for something like this, but if I remember correctly, v2 had a console that you could run yourself. Is GraphiQL the extent of v3 console functionality?

AFAIK console needs the control plane, which means you need LUX for it? I'm not entirely clear on this.

In a perfect world, this repo would contain a Dockerfile that could clone the console repository and then setup and run the console from scratch. This might require some interplay between the directory that contains lux, and the env variables may need editted.

I was working with setting up the LUX control plane locally, but having issues.

