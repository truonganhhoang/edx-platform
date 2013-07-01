class @TabsEditorDescriptor
  @isInactiveClass : "is-inactive"

  constructor: (element) ->
    @element = element;
    @$tabs = $(".tab", @element)
    @$content = $(".component-tab", @element)

    @element.on('click', '.editor-tabs .tab', @onSwitchEditor)

    # If default visible tab is not setted or if were marked as current
    # more than 1 tab just first tab will be shown
    if @$tabs.filter('.current').length isnt 1
      @$tabs.first().trigger("click", [true])

   onSwitchEditor: (e, reset) =>
    e.preventDefault();

    isInactiveClass = TabsEditorDescriptor.isInactiveClass
    $currentTarget = $(e.currentTarget)

    if not $currentTarget.hasClass('current') or reset is true

      @$tabs.removeClass('current')
      $currentTarget.addClass('current')

      # Tabs are implemeted like anchors. Therefore we can use hash to find corresponding content
      content_id = $currentTarget.attr('href')

      @$content
        .addClass(isInactiveClass)
        .filter(content_id)
        .removeClass(isInactiveClass)

      @$tabs.closest('.wrapper-comp-editor').trigger(
        'TabsEditor',  # event
        [
          $currentTarget.text(), # tab_name
          content_id  # tab_id
        ]
      )

  save: ->
    @element.off('click', '.editor-tabs .tab', @onSwitchEditor)