export default async function handleFetch(name, api) {
    if (localStorage.getItem(name)) {
      console.log("exists", localStorage.getItem(name));
      return JSON.parse(localStorage.getItem(name));
    } else {
      let response = await fetch(api);
      response = await response.json();
      localStorage.setItem(name, JSON.stringify(response));
      console.log("not", localStorage.getItem(name));
      return JSON.parse(localStorage.getItem(name));
    }
  }
  