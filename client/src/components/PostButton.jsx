import { Button } from "react-bootstrap";

export default function PostButton({
  variant,
  checkedList,
  disabledBy,
  children
}) {
  return (
    <Button
      variant={variant}
      disabled={
        checkedList["length"] === 0 ||
        checkedList.flat().some((el) => disabledBy.includes(el))
      }
    >
      {children}
    </Button>
  );
}
