<template>
  <div class="col-md-4">
    <div class="card text-center shadow-sm p-3">
      <h3>{{ value }}</h3>
      <p>{{ label }}</p>
    </div>
  </div>
</template>

<script>
export default {
  props: ['value', 'label']
}
</script>