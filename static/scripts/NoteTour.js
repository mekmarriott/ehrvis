
var initNoteTour = function() {
  $("#demo-start-page").fadeOut(200);
  console.log("Starting tour...");
  noteSteps = [
    {
      element: "#note_plot_target",
      title: "Note Chart",
      content: "This note chart displays...",
      placement: "top",
    },
    {
      element: ".legend",
      title: "Note Timeline Legend",
      content: "This is the legend for the note timeline...",
      placement: "left",
    },
        {
      element: "#inpatientkey",
      title: "Note Timeline Legend",
      content: "This is the legend for the note timeline...",
      placement: "bottom",
    },
    {
      element: "#note_nav_target",
      title: "Note Navigation",
      content: "This is the overview of the patient's entire recorded medical history...",
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