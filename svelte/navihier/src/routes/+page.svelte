<script>
  import { redirect } from '@sveltejs/kit';
  import { base } from '$app/paths';

  redirect(307, `${base}/pick`);
</script>