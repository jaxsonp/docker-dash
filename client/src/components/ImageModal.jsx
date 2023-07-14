import { Button } from "react-bootstrap";
import { Modal } from "react-bootstrap";
import { Form } from "react-bootstrap";
import ReactJson from "@microlink/react-json-view";
import { useRef } from "react";

const api = "http://192.168.98.74/api/demo/";

export default function ImportModal(props) {
  const imageRef = useRef();
  const reasonRef = useRef();

  return (
    <Modal
      {...props}
      size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered
    >
      <Modal.Header closeButton style={{ background: "gainsboro" }}>
        <Modal.Title
          id="contained-modal-title-vcenter"
          style={{ width: "100%", textAlign: "center" }}
        >
          Image Request Center
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <h4>Which dockerhub image are you looking for?</h4>
        <Form.Control ref={imageRef} type="text"></Form.Control>
        <h4>Reasons for Request:</h4>
        <Form.Control ref={reasonRef} as="textarea" rows={3}></Form.Control>
      </Modal.Body>
      <Modal.Footer>
        <div style={{ margin: "auto" }}>
          <Button
            style={{ marginRight: "50px" }}
            onClick={async () => {
              // try {
              let response = await fetch(
                api + "request-image?image=" + imageRef.current.value,
                {
                  method: "POST",
                }
              );
              console.log("b4", response);
              response =
                typeof response === "string"
                  ? JSON.stringify(response)
                  : await response.json();
              console.log("after", response);
              alert("200 Request Successful");
              // } catch (err) {
              //   alert("Something went wrong...");
              //   console.error(err);
              // }
              imageRef.current.value = "";
              reasonRef.current.value = "";
            }}
          >
            Submit
          </Button>
          <Button variant="warning" onClick={() => props.onHide()}>
            Cancel
          </Button>
        </div>
      </Modal.Footer>
    </Modal>
  );
}

export function DangerModal(props) {
  return (
    <Modal
      {...props}
      size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered
    >
      <Modal.Header closeButton style={{ background: "gainsboro" }}>
        <Modal.Title
          id="contained-modal-title-vcenter"
          style={{ width: "100%", textAlign: "center" }}
        >
          Do you want to remove selected app(s)?
        </Modal.Title>
      </Modal.Header>
      <Modal.Footer>
        <div style={{ margin: "auto" }}>
          <Button
            style={{ marginRight: "50px" }}
            onClick={async () => {
              props.onHide();
              await props.handleBatchPost();
            }}
          >
            Yes
          </Button>
          <Button variant="warning" onClick={() => props.onHide()}>
            No
          </Button>
        </div>
      </Modal.Footer>
    </Modal>
  );
}

export function InspectModal(props) {
  return (
    <Modal
      {...props}
      size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered
    >
      <Modal.Header closeButton style={{ background: "gainsboro" }}>
        <Modal.Title
          id="contained-modal-title-vcenter"
          style={{ width: "100%", textAlign: "center" }}
        >
          {"<server.hostname>"}
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <ReactJson
          style={{
            textAlign: "left",
            wordBreak: "break-all",
          }}
          collapsed={false}
          src={props.src}
        />
      </Modal.Body>
    </Modal>
  );
}
