import { useState, useEffect } from "react";
import { Button, Card, Pagination, Spinner } from "react-bootstrap";
// import { useNavigate } from "react-router-dom";
import { ChevronDown, ChevronUp } from "react-feather";
import { InspectModal } from "./ImageModal";
import servers from "../serverInfo.json";
import clustersLocal from "../clusters.json";

const renderPagination = (items, step, selectedIndex, setSelectedIndex) => {
  let pages = [];
  for (let i = 1; i <= Math.ceil(items / step); i++) {
    pages.push(
      <Pagination.Item
        active={selectedIndex === i}
        onClick={() => setSelectedIndex(i)}
        key={i}
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
  let sorted = multiObj
    .filter((el) => el.length > 1)
    .sort((a, b) => b.length - a.length);
  if (multiObj !== 0) {
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
    sorted = sorted.concat(singElArr);
  }
  sorted = sorted.concat(multiObj);
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
  const [selectedIndex, setSelectedIndex] = useState(1);
  const [numItems, setNumItems] = useState(1);
  const [expanded, setExpanded] = useState(null);
  const [modalShow, setModalShow] = useState(false);
  const [initialData, setInitialData] = useState([]);
  const [inspectInfo, setInspectInfo] = useState("");
  const [reorderedData, setReorderedData] = useState([]);
  const [timeOfLastFetch, setTimeOfLastFetch] = useState(Date.now());
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    sessionStorage.removeItem("sortedData");

    async function getServerPreviews() {
      async function fetchClusterData() {
        try {
          const nodes = await fetch(api + "get-node-status");
          let nodesJ = await nodes.json();
          console.log(nodesJ);
          return sortSpecificData(servers, [nodesJ]);
        } catch (err) {
          setFailed(true);
          console.error(err);
        }
      }
      setInitialData(await fetchClusterData());
      let timer = setInterval(async () => {
        if (!sessionStorage.getItem("sortedData")) {
          try {
            const nodes = await fetch(api + "get-node-status");
            let nodesJ = await nodes.json();
            let sorted = sortSpecificData(servers, [nodesJ]);
            sessionStorage.setItem("sortedData", JSON.stringify(sorted));
            setInitialData(sorted);
          } catch (err) {
            setFailed(true);
            console.error(err);
          }
        } else {
          setInitialData(JSON.parse(sessionStorage.getItem("sortedData")));
          if (timeOfLastFetch + 600000 < Date.now()) {
            setTimeOfLastFetch(Date.now());
            sessionStorage.removeItem("sortedData");
          }
        }
      }, 600000);
      return function () {
        clearTimeout(timer);
      };
    }
    getServerPreviews();
  }, []);

  useEffect(() => {
    setNumItems(initialData.length);
  }, [initialData.length]);

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
    let response = await fetch(endpoint);
    response = await response.json();
    setInspectInfo(response);
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
                  key={index}
                  style={{
                    width: card.length > 1 ? "428px" : "214px",
                    height: "fit-content",
                  }}
                >
                  <h4 style={{ margin: "10px", fontSize: "22px" }}>
                    {card[0].ManagerStatus === "Leader" || card.length > 1
                      ? "Cluster Host"
                      : "Container Host"}
                  </h4>
                  <div
                    style={{
                      backgroundColor:
                        card[0].state === "on" ||
                        (card[0].ManagerStatus === "Leader" &&
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
                              key={key}
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
                                      {inner.ManagerStatus || "Worker"}
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
                                    <p>{inner.Hostname}</p>
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
                                    {/* Status, Availability */}
                                    <p>{inner["Hostname"]}</p>
                                    <hr />
                                    <p>CPU%: {inner["CPU%"]}</p>
                                    <p>Mem%: {inner["Memory%"]}</p>
                                    <p>User Num: {inner["User Quantity"]}</p>
                                    <p>
                                      Container Qty:{" "}
                                      {inner["Container Quantity"]}
                                    </p>
                                  </>
                                )}
                              </div>
                            </Card.Body>
                            {card.length > 1 && (
                              <Button
                                onClick={() => {
                                  handleInspectModal(api + "get-node-info");
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
