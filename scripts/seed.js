const database = db.getSiblingDB("project_db");

const records = [
  {
    _id: "mock-001",
    label: "cup",
    confidence: 0.94,
    captured_at: new Date("2026-11-24T14:00:00Z"),
    source: "mock"
  },
  {
    _id: "mock-002",
    label: "book",
    confidence: 0.88,
    captured_at: new Date("2026-11-24T14:01:00Z"),
    source: "mock"
  }
];

records.forEach((record) => {
  database.predictions.replaceOne(
    { _id: record._id },
    record,
    { upsert: true }
  );
});

print("Mock records:");
printjson(
  database.predictions.find({ source: "mock" }).toArray()
);