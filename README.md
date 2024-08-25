# simple-web-archiver
Designed for archiving simple (mostly static html) websites that host stories.

It's very primitive. 
Works by downloading and parsing the first page, extracting all links (of the same domain),
and repeating the process again until all links have been visited and downloaded.

Doesn't archive style-sheets or scripts. 
There's just a cheap replacement of the /theme links with original's website host.

## How to use
You need docker installed.

Create .env-local file next to the .env file. Set values in it based on the .env file. 
* `base_url` - what's the base url of the website you're archiving eg. example.org
* `url_to_start_with` - what page to start downloading from
* `paths_to_exclude` - excludes all links that contain those phrases - useful for avoiding search links or never
  ending chain links

Use `docker compose run --rm python` to run the archiver after setting up the env file.

It's all single-threaded so it might take a while. 
Keep an eye on it in case in ends up in a never ending loop or download something not useful like search by tags links.
Modify to your needs.