export default async function handleFetch(name, api) {
  if (sessionStorage.getItem(name)) {
    return JSON.parse(sessionStorage.getItem(name));
  } else {
    try {
      let response = await fetch(api);
      response = await response.json();
      sessionStorage.setItem(name, JSON.stringify(response));
      return JSON.parse(sessionStorage.getItem(name));
    } catch (err) {
      throw new Error(err);
    }
  }
}
