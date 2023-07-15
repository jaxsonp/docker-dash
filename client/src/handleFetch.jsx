export default async function handleFetch(name, api) {
  if (sessionStorage.getItem(name)) {
    return JSON.parse(sessionStorage.getItem(name));
  } else {
    let response = await fetch(api);
    response = await response.json();
    if (typeof response === "object") {
      console.log("ok");
      sessionStorage.setItem(name, JSON.stringify(response));
      return JSON.parse(sessionStorage.getItem(name));
    }
  }
}
