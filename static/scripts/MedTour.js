
var initMedTour = function() {
  $("#demo-start-page").fadeOut(200);
  console.log("Starting tour...");
  noteSteps = [
    {
      element: "#med_plot_target",
      title: "Medication Chart",
      content: "This chart plots a patient's medications on a timeline.",
      placement: "bottom",
    },
    {
      element: "#med_plot_target",
      title: "Medication Chart",
      content: "Thicker lines mean higher dose, in relative terms for each drug.",
      placement: "bottom",
    },
    {
      element: "#med_plot_target",
      title: "Medications",
      content: "The points marking the ends of intervals are interactive. Try hovering the mouse over a point...",
      placement: "bottom",
      reflex: true,
    },  
    {
      element: "#tooltip-replacement",
      title: "Medication Details",
      content: "...and further information can be seen on the panel above after hovering over a point.",
      placement: "bottom",
    },
    {
      element: "#med_plot_target",
      title: "Medication Axis",
      content: "Medication names are previewed on the y-axis...",
      placement: "bottom",
    },
    {
      element: "#med_plot_target",
      title: "Medications",
      content: "Medication lists can be long, so not all medications may be shown.",
      placement: "bottom",
    },
    {
      element: "#med_plot_target",
      title: "Medications",
      content: "Zoom (scroll) or pan (click and drag) to see other times or medications",
      placement: "bottom",
    },
    {
      element: "#med_nav_target",
      title: "Full timeline",
      content: "The lower timeline spans the entire prescription history.",
      placement: "top",
    },
    {
      element: "#med_nav_target",
      title: "Full timeline",
      content: "Drag the selection window slider, or simply click on a region of interest to jump there on the main timeline.",
      placement: "top",
    },
    {
      element: "#navbar-hold",
      title: "Next Steps",
      content: "When you're done exploring the medication demo, you can use this navigation bar to go to the note demo or the timelines for the sample case.",
      placement: "bottom",
      reflex: true
    },
    {
      element: "#med_plot_target",
      title: "",
      content: "Click on the main timeline to wrap up",
      placement: "top",
      reflex: true
    },
  ]

  // Instance the tour
  var MedTour = new Tour({
    name: "med-tour",
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
  // Initialize the tour
  MedTour.init();
  // Start the tour
  MedTour.start();
}