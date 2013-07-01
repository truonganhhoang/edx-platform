class @TabsEditorDescriptor
  @isInactiveClass : "is-inactive"

  constructor: (element) ->
    @element = element;
    @$tabs = $(".tab", @element)
    @$content = $(".component-tab", @element)

    @element.on('click', '.editor-tabs .tab', @onSwitchEditor)

    if not @$tabs.find('.current').length
      @$tabs.first().trigger("click", 'id')

   onSwitchEditor: (e) =>
    e.preventDefault();

    isInactiveClass = TabsEditorDescriptor.isInactiveClass
    $currentTarget = $(e.currentTarget)
    if not $currentTarget.hasClass('current')

      @$tabs.removeClass('current')
      $currentTarget.addClass('current')

      # Tabs are implemeted like anchors. Therefore we can use hash to find corresponding content
      hash = $currentTarget.attr('href')
      @$content
        .addClass(isInactiveClass)
        .filter(hash)
        .removeClass(isInactiveClass)

      @$tabs.trigger('TabsEditorDescriptor-idashdjhasdasd', '#{hash}')

  save: ->
    @element.off('click', '.editor-tabs .tab', @onSwitchEditor)