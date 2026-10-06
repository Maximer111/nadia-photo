// Search Console wants the verification file at its exact .html path with a 200;
// asset handling would 307 it to the extensionless URL.
export default {
  fetch(req, env) {
    const url = new URL(req.url);
    url.pathname = url.pathname.replace(/\.html$/, "");
    return env.ASSETS.fetch(new Request(url, req));
  },
};
