define ['underscore'], ({template}) ->

  graphRow: template '
    <div class="graph-row">
      <div class="header">
        <span class="icon icon-visible">▼</span>
        <span class="icon icon-collapsed">►</span>
        <span class="caption"><%= caption %></span></div>
      <div class="content"></div>
    </div>
  '
