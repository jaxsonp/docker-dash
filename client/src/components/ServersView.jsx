import { useState, useEffect } from "react";
import { Button, Card, Pagination, Spinner } from "react-bootstrap";
import { ChevronDown, ChevronUp } from "react-feather";
import { InspectModal } from "./ImageModal";
import servers from "../serverInfo.json";
//TESTING
import appStats from "../app-stats.json";
import handleFetch from "../handleFetch";

const renderPagination = (items, step, selectedIndex, setSelectedIndex) => {
  let pages = [];
  for (let i = 1; i <= Math.ceil(items / step); i++) {
    pages.push(
      <Pagination.Item
        active={selectedIndex === i}
        onClick={() => setSelectedIndex(i)}
        key={"pg" + i}
      >
        {i}
      </Pagination.Item>
    );
  }
  return pages;
};

const api = "http://192.168.98.74/api/demo/";
const step = 3;

function sortSpecificData(singleObj, multiObj) {
  let singElArr = singleObj.map((server) => [server]);
  let sorted = null;
  if (multiObj) {
    sorted = multiObj.filter(
      (el) =>
        el.length > 1 ||
        el[0].ManagerStatus === "Leader" ||
        el[0].ManagerStatus === "Solo"
    );
    if (sorted.length > 1) {
      sorted = sorted.sort((a, b) => b.length - a.length);
      sorted.map((el) => {
        return el.sort((a, b) => {
          if (a.ManagerStatus.length === 0 || b.ManagerStatus.length === 0) {
            if (a.ManagerStatus.length === 0 && b.ManagerStatus.length === 0) {
              return 0;
            } else if (a.ManagerStatus.length === 0) {
              return 1;
            } else {
              return -1;
            }
          } else {
            return a.ManagerStatus.length - b.ManagerStatus.length;
          }
        });
      });
    }
    sorted = sorted.concat(singElArr);
  } else {
    sorted = singElArr;
  }
  sorted.sort((a, b) => {
    if (
      b[0].Status === "failed" ||
      b[0].ManagerStatus === "" ||
      b[0].state === "off"
    ) {
      return 1;
    } else if (
      a[0].Status === "failed" ||
      a[0].ManagerStatus === "" ||
      a[0].state === "off"
    ) {
      return -1;
    }
    return 0;
  });
  return sorted;
}

function ServersView() {
  const [soloAppStats, setSoloAppStats] = useState([]);
  const [soloNode, setSoloNode] = useState({});
  const [selectedIndex, setSelectedIndex] = useState(1);
  const [numItems, setNumItems] = useState(1);
  const [expanded, setExpanded] = useState(null);
  const [modalShow, setModalShow] = useState(false);
  const [initialData, setInitialData] = useState([]);
  const [inspectInfo, setInspectInfo] = useState(null);
  const [reorderedData, setReorderedData] = useState([]);
  const [timeOfLastFetch, setTimeOfLastFetch] = useState(Date.now());
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    // async function fetchClusterData() {
    //   try {
    //     const nodes = await fetch(api + "get-node-status");
    //     let nodesJ = await nodes.json();
    //     return sortSpecificData(servers, [nodesJ]);
    //   } catch (err) {
    //     setFailed(true);
    //     console.error(err);
    //   }
    // }
    // async function getServerPreviews() {
    //   setInitialData(await fetchClusterData());
    //   let timer = setInterval(async () => {
    //     if (!sessionStorage.getItem("sortedData")) {
    //       try {
    //         const nodes = await fetch(api + "get-node-status");
    //         let nodesJ = await nodes.json();
    //         let sorted = sortSpecificData(servers, [nodesJ]);
    //         sessionStorage.setItem("sortedData", JSON.stringify(sorted));
    //         setInitialData(sorted);
    //       } catch (err) {
    //         setFailed(true);
    //         console.error(err);
    //       }
    //     } else {
    //       setInitialData(JSON.parse(sessionStorage.getItem("sortedData")));
    //       if (timeOfLastFetch + 600000 < Date.now()) {
    //         setTimeOfLastFetch(Date.now());
    //         sessionStorage.removeItem("sortedData");
    //       }
    //     }
    //   }, 600000);
    //   return function () {
    //     clearTimeout(timer);
    //   };
    // }
    // getServerPreviews();
    let allAccounted = [...servers, soloNode];
    let initialData = sortSpecificData(allAccounted);
    setInitialData(initialData);
  }, [soloNode]);

  useEffect(() => {
    const appStats = async () => {
      await handleFetch("appStats", api + "get-app-stats");
      setSoloAppStats(JSON.parse(sessionStorage.getItem("appStats")));
    };
    appStats();
    let interval = setInterval(async () => {
      sessionStorage.removeItem("appStats");
      let appStats = await handleFetch("appStats", api + "get-app-stats");
      setSoloAppStats(JSON.parse(appStats));
    }, 300000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    let memPerc = 0;
    let cpuPerc = 0;
    let appLength = appStats.length;
    let userLength = 0;
    let AppNames = [];
    soloAppStats.forEach((el) => {
      memPerc += parseFloat(el.MemPerc);
      cpuPerc += parseFloat(el.CPUPerc);
      AppNames.push(el.Name);
    });
    let named = [];
    AppNames.forEach((name) => {
      let ind = name.indexOf("--");
      if (ind === -1) {
        !named.includes("anon") && named.push("anon");
      } else {
        let sub = name.substring(ind + 2, name.length);
        if (!named.includes(sub)) {
          named.push(sub);
        }
      }
    });
    userLength = named.length;
    let solo = {
      Hostname: "ondemand",
      "Memory%": memPerc.toFixed(2) + "%",
      "CPU%": cpuPerc.toFixed(2) + "%",
      "Current Apps": appLength,
      Users: userLength,
    };
    setSoloNode(solo);
  }, [soloAppStats]);

  useEffect(() => {
    setNumItems(initialData && initialData.length ? initialData.length : 1);
  }, [initialData]);

  useEffect(() => {
    if (initialData && initialData.length) {
      let displayedCards = initialData.slice(
        selectedIndex * step - step,
        selectedIndex * step
      );
      setReorderedData(displayedCards || initialData);
    }
  }, [initialData, selectedIndex, numItems]);

  async function handleInspectModal(endpoint) {
    try {
      let response = await fetch(endpoint);
      response = await response.json();
      setInspectInfo(response);
    } catch (err) {
      console.error(err);
      setInspectInfo([{ message: "Something went wrong..." }]);
    }
  }

  return (
    <>
      <InspectModal
        show={modalShow}
        onHide={() => setModalShow(false)}
        src={inspectInfo}
      />
      <div
        style={{
          width: "100%",
          textAlign: "left",
        }}
      >
        <h2 style={{ textAlign: "center" }}>SERVERS:</h2>
        <br />
        <div
          style={{
            width: "100%",
            display: "flex",
            flexWrap: "wrap",
            gap: "15px",
            justifyContent: "center",
          }}
        >
          {reorderedData?.length ? (
            reorderedData.map((card, index) => {
              return (
                <Card
                  key={"ro" + index}
                  style={{
                    width: card.length > 1 ? "428px" : "214px",
                    height: "fit-content",
                  }}
                >
                  <h4 style={{ margin: "10px", fontSize: "22px" }}>
                    {card[0].ManagerStatus === "Leader" || card.length > 1
                      ? "Swarm Server(s)"
                      : "Solo Server"}
                  </h4>
                  <div
                    style={{
                      backgroundColor:
                        card[0].state === "on" ||
                        ((card[0].ManagerStatus === "Leader" ||
                          card[0].ManagerStatus === "Solo") &&
                          card[0].Status === "Ready" &&
                          card[0].Availability === "Active")
                          ? "green"
                          : "red",
                      borderRadius: "50%",
                      width: "20px",
                      height: "20px",
                      position: "absolute",
                      top: "10px",
                      right: "10px",
                    }}
                  ></div>
                  <div
                    style={{
                      display: "grid",
                      gap: "20px",
                      gridTemplateColumns: card.length > 1 ? "1fr 1fr" : "1fr",
                      padding: "10px",
                      height: expanded === index + 1 ? "fit-content" : "346px",
                      overflow: "hidden",
                    }}
                  >
                    {card.length > 4 && (
                      <span
                        className="reenter"
                        style={{
                          position: "absolute",
                          left: 10,
                          top: 36,
                          opacity: expanded ? 0 : 1,
                        }}
                      >
                        Health of Not Visible:
                      </span>
                    )}
                    {card.map((inner, key) => {
                      return (
                        <>
                          {card.length > 4 && (
                            <div
                              style={{
                                position: "absolute",
                                left: 165,
                                top: 41,
                              }}
                              key={"card" + key}
                            >
                              {key > 3 && (
                                <div
                                  className="reenter"
                                  style={{
                                    width: "14px",
                                    backgroundColor:
                                      inner.ManagerStatus === "Unavailable" ||
                                      inner.Status === "failed"
                                        ? "orangered"
                                        : inner.Availability === "paused" ||
                                          inner.Availability === "drain"
                                        ? "hsl(56, 100%, 50%)"
                                        : "green",
                                    height: "14px",
                                    marginLeft: 30 * (key - 4) + "px",
                                    borderRadius: "50%",
                                    opacity: expanded ? 0 : 1,
                                  }}
                                ></div>
                              )}
                            </div>
                          )}
                          <Card
                            style={{
                              height: "fit-content",
                              marginTop: "10px",
                            }}
                          >
                            <Card.Body>
                              <div
                                className="server-card-mapped-info"
                                style={{ margin: "5px 10px" }}
                              >
                                {inner.Availability ? (
                                  <>
                                    <h5
                                      style={{
                                        color:
                                          inner.ManagerStatus === "Unavailable"
                                            ? "orangered"
                                            : "unset",
                                      }}
                                    >
                                      {inner.ManagerStatus !== "Solo"
                                        ? inner.ManagerStatus || "Worker"
                                        : inner.Hostname}
                                    </h5>
                                    <div
                                      style={{
                                        backgroundColor:
                                          inner.ManagerStatus ===
                                            "Unavailable" ||
                                          inner.Status === "failed"
                                            ? "orangered"
                                            : inner.Availability === "paused" ||
                                              inner.Availability === "drain"
                                            ? "hsl(56, 100%, 50%)"
                                            : "green",
                                        borderRadius: "50%",
                                        width: "15px",
                                        height: "15px",
                                        position: "absolute",
                                        top: "10px",
                                        right: "10px",
                                      }}
                                    ></div>
                                    {inner.ManagerStatus !== "Solo" && (
                                      <p>{inner.Hostname}</p>
                                    )}
                                    <hr style={{ margin: "8px 0" }} />
                                    <p
                                      style={{
                                        color:
                                          inner.Availability === "paused" ||
                                          inner.Availability === "drain"
                                            ? "hsl(56, 100%, 44%)"
                                            : "unset",
                                      }}
                                    >
                                      Availability: {inner.Availability}
                                    </p>
                                    <p
                                      style={{
                                        color:
                                          inner.Status === "failed"
                                            ? "orangered"
                                            : "unset",
                                      }}
                                    >
                                      Status: {inner.Status}
                                    </p>
                                  </>
                                ) : (
                                  <>
                                    <h5>{inner["Hostname"]}</h5>
                                    <hr />
                                    <p>CPU%: {inner["CPU%"]}</p>
                                    <p>Mem%: {inner["Memory%"]}</p>
                                    <p>Users: {inner["Users"]}</p>
                                    <p>Current Apps: {inner["Current Apps"]}</p>
                                  </>
                                )}
                              </div>
                            </Card.Body>
                            {(card[0].ManagerStatus === "Leader" ||
                              card.length > 1) && (
                              <Button
                                onClick={() => {
                                  handleInspectModal(
                                    api +
                                      "get-node-info?hostname=" +
                                      inner.Hostname
                                  );
                                  setModalShow(true);
                                }}
                                style={{ margin: "0 auto 10px" }}
                              >
                                Inspect
                              </Button>
                            )}
                          </Card>
                        </>
                      );
                    })}
                  </div>
                  {card.length > 2 && (
                    <button
                      className="hover"
                      style={{
                        fontSize: "20px",
                        width: "fit-content",
                        margin: "0 auto",
                      }}
                      onClick={() => {
                        expanded === index + 1
                          ? setExpanded(null)
                          : setExpanded(index + 1);
                      }}
                    >
                      {expanded === index + 1 ? <ChevronUp /> : <ChevronDown />}
                    </button>
                  )}
                  <Button
                    onClick={() =>
                      alert(
                        "This would redirect to " +
                          (card[0].Hostname || "<hostname>") +
                          " apps"
                      )
                    }
                    style={{
                      margin: card.length > 2 ? "10px" : "44px 10px 10px",
                    }}
                  >
                    View Current Apps
                  </Button>
                </Card>
              );
            })
          ) : !failed ? (
            <div style={{ height: "484px" }}>
              <Spinner animation="border" />
            </div>
          ) : (
            <h1 style={{ color: "crimson" }}>SERVERS DOWN</h1>
          )}
        </div>
        {initialData?.length && (
          <Pagination
            style={{
              width: "fit-content",
              margin: "20px auto",
              display: "flex",
              justifyContent: "center",
            }}
            onClick={() => setExpanded(null)}
          >
            <Pagination.First
              onClick={() => {
                setSelectedIndex(1);
              }}
            />
            <Pagination.Prev
              onClick={() =>
                selectedIndex > 1 && setSelectedIndex(selectedIndex - 1)
              }
            />
            {renderPagination(numItems, step, selectedIndex, setSelectedIndex)}
            <Pagination.Next
              onClick={() =>
                selectedIndex < Math.ceil(initialData.length / step) &&
                setSelectedIndex(selectedIndex + 1)
              }
            />
            <Pagination.Last
              onClick={() =>
                setSelectedIndex(Math.ceil(initialData.length / step))
              }
            />
          </Pagination>
        )}
      </div>
    </>
  );
}

export default ServersView;
