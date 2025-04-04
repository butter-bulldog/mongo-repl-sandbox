rs.initiate({
  _id: 'rs0',
  members: [
    {
      _id: 0,
      host: "mongodb24-primary:27017",
      priority: 100
    },
    {
      _id: 1,
      host: "mongodb24-secondary:27017",
      priority: 10
    },
    {
      _id: 2,
      host: "mongodb24-arbiter:27017",
      arbiterOnly: true
    }
  ],
});
