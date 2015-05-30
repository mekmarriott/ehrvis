
var initNoteTour = function() {
  $("#demo-start-page").fadeOut(200);
  console.log("Starting tour...");
  noteSteps = [
    {
      element: "#note_plot_target",
      title: "Note Chart",
      content: "This chart plots patient on a timeline.",
      placement: "top",
    },
    {
      element: ".legend",
      title: "Note Timeline Legend",
      content: "Notes are color-coded by type",
      placement: "left",
    },
    {
      element: "#inpatientkey",
      title: "Note Timeline Legend",
      content: "Additionally, the background of the chart has shaded regions...",
      placement: "bottom",
    },
    {
      element: "#inpatientkey",
      title: "Note Timeline Legend",
      content: "...which represent inpatient and outpatient periods in the medical record.",
      placement: "bottom",
    },
    {
      element: "#note_plot_target",
      title: "Note Chart",
      content: "The main plot show a focused portion of the patient's record.",
      placement: "top",
    },
    {
      element: "#note_plot_target",
      title: "Note Chart",
      content: "To change the viewing region, scroll to zoom in/out...",
      placement: "top",
    },
    {
      element: "#note_plot_target",
      title: "Note Chart",
      content: "...or click and drag left/right to pan.",
      placement: "top",
    },
    {
      element: "#note_nav_target",
      title: "Note Navigation",
      content: "The naviagation strip below displays the entire recorded medical history...",
      placement: "top"
    },
    {
      element: "#note_nav_target",
      title: "Note Navigation",
      content: "...and can be used for quick naviagation. Try moving the selection window along the lower timeline.",
      placement: "top"
    },
    {
      element: "#choices",
      title: "Note Filtering",
      content: "This is a filtering selection for the note timeline...try clicking on the different selections to toggle displays of different types of patient notes.",
      placement: "bottom",
      reflex: true
    }
  ]

  // Instance the tour
  var NoteTour = new Tour({
    name: "note-tour",
    steps: noteSteps,
    container: "body",
    keyboard: true,
    storage: false,
    debug: false,
    backdrop: true,
    backdropContainer: 'body',
    backdropPadding: 10,
    redirect: true,
    orphan: false,
    duration: false,
    delay: false,
    basePath: "",
    // template: templateString,
    afterGetState: function (key, value) {},
    afterSetState: function (key, value) {},
    afterRemoveState: function (key, value) {},
    onStart: function (tour) {},
    onEnd: function (tour) {},
    onShow: function (tour) {},
    onShown: function (tour) {},
    onHide: function (tour) {},
    onHidden: function (tour) {},
    onNext: function (tour) {},
    onPrev: function (tour) {},
    onPause: function (tour, duration) {},
    onResume: function (tour, duration) {},
    onRedirectError: function (tour) {}
  });
  console.log("launching???");
  // Initialize the tour
  NoteTour.init();
  console.log("OK");
  // Start the tour
  NoteTour.start();
}