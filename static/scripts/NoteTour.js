
function startNoteTour() {
  noteSteps = [
    {
      element: "#note_plot_target",
      title: "Note Chart",
      content: "This is the note chart..."
    },
    {
      element: "#note_nav_target",
      title: "Note Navigation",
      content: "This is the overview of the patient's entire recorded medical history..."
    }
  ]

  // templateString = "<div class='popover tour'><div class='arrow'></div><h3 class='popover-title'></h3><div class='popover-content'></div><div class='popover-navigation'><button class='btn btn-default' data-role='prev'>« Prev</button><span data-role='separator'>|</span><button class='btn btn-default' data-role='next'>Next »</button></div><button class='btn btn-default' data-role='end'>End tour</button></nav></div>"
  // Instance the tour
  var NoteTour = new Tour({
    name: "note-tour",
    steps: noteSteps,
    container: "body",
    keyboard: true,
    storage: window.localStorage,
    debug: false,
    backdrop: true,
    backdropContainer: 'body',
    backdropPadding: 0,
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
  NoteTour.init();

  // Start the tour
  NoteTour.start();
}