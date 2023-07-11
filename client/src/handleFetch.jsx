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
  
  export async function handleFetchInterval(name, api, interval) {
    let timer = setInterval(async () => {
      if (!localStorage.getItem(name)) {
        let response = await fetch(
          api
        );
        response = await nodes.json();
        localStorage.setItem(name, JSON.stringify(response));
        return JSON.parse(localStorage.getItem(name));
      } else {
        return JSON.parse(localStorage.getItem("sortedData"));
        if (timeOfLastFetch + interval < Date.now()) {
          setTimeOfLastFetch(Date.now());
          localStorage.clear(name);
        }
      }
    }, interval);
    return function () {
      clearTimeout(timer);
    };
  }