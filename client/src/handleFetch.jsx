export default async function handleFetch(name, api) {
  if (sessionStorage.getItem(name)) {
    return JSON.parse(sessionStorage.getItem(name));
  } else {
    try {
      let response = await fetch(api);
      response = await response.json();
      sessionStorage.setItem(name, JSON.stringify(response));
      JSON.parse(sessionStorage.getItem(name));
      alert("Your request was successed");
    } catch (err) {
      alert(err);
      throw new Error(err);
    }
  }
}

// export async function handleFetchInterval(name, api, interval) {
//   let timeOfLastFetch = Date.now();
//   let timer = setInterval(async () => {
//     if (!sessionStorage.getItem(name)) {
//       let response = await fetch(api);
//       response = await nodes.json();
//       sessionStorage.setItem(name, JSON.stringify(response));
//       return JSON.parse(sessionStorage.getItem(name));
//     } else {
//       let parsed = JSON.parse(sessionStorage.getItem(name));
//       if (timeOfLastFetch + interval < Date.now()) {
//         timeOfLastFetch = Date.now();
//         sessionStorage.removeItem(name);
//       }
//       return parsed;
//     }
//   }, interval);
//   return function () {
//     clearTimeout(timer);
//   };
// }
